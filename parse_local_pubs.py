#!/usr/bin/env python3
"""
parse_local_pubs.py

Reads the .htm/.html pub pages you saved locally (via the Edge/Chrome VBA
macro) and extracts the same fields the network scraper would have
pulled out -- name, phone, address, postcode, coordinates, opening
hours, facilities, hotel flag, history, photos, menu link -- into a CSV,
JSON, and SQLite database.

This does NOT make any network requests. It only reads files already
sitting on your disk, so there's nothing to rate-limit or worry about
blocking.

USAGE
-----
    pip install beautifulsoup4

    python parse_local_pubs.py "C:\\Users\\user\\OneDrive\\Documents\\Business\\Wetherspoon Database"

    (Or just run it with no argument and it'll prompt you for the folder.)

This is safe to re-run any time you save more pages with the VBA macro --
it rebuilds the CSV/JSON/database from whatever's currently in the folder,
each time.

OUTPUT
------
    wetherspoon_pubs_local.csv
    wetherspoon_pubs_local.json
    wetherspoon_pubs_local.db     (SQLite, table name "pubs")

written into the same folder you point it at.
"""

import json
import os
import re
import sqlite3
import sys
from dataclasses import dataclass, field
from typing import Optional

from bs4 import BeautifulSoup

BASE_URL = "https://www.jdwetherspoon.com"
DAY_NAMES = [
    "Monday", "Tuesday", "Wednesday", "Thursday",
    "Friday", "Saturday", "Sunday",
]


# --------------------------------------------------------------------------
# Data model
# --------------------------------------------------------------------------

@dataclass
class Pub:
    source_file: str
    url: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    postcode: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    has_hotel: bool = False
    menu_url: Optional[str] = None
    history: Optional[str] = None
    facilities: list = field(default_factory=list)
    opening_hours: dict = field(default_factory=dict)
    photos: list = field(default_factory=list)
    parsed_ok: bool = False
    error: Optional[str] = None


# --------------------------------------------------------------------------
# Field extraction (same logic as the network scraper, adapted for local
# files -- e.g. the URL is reconstructed from the filename since there's
# no request URL to read it from directly)
# --------------------------------------------------------------------------

def slug_to_url(slug: str) -> str:
    return f"{BASE_URL}/pubs/{slug}/"


def parse_name(soup: BeautifulSoup) -> Optional[str]:
    h1 = soup.find("h1")
    return h1.get_text(strip=True) if h1 else None


def parse_phone(soup: BeautifulSoup) -> Optional[str]:
    tel = soup.select_one('a[href^="tel:"]')
    if tel:
        return tel.get_text(strip=True) or tel["href"].replace("tel:", "")
    return None


def parse_address_and_postcode(soup: BeautifulSoup):
    directions = soup.find("a", href=re.compile(r"maps\.google\.com"))
    address = None
    if directions:
        parent = directions.find_parent()
        if parent:
            text = parent.get_text(" ", strip=True)
            text = re.sub(r"Get directions to.*$", "", text).strip()
            address = text or None
    if not address and directions and "q=" in directions.get("href", ""):
        from urllib.parse import unquote, urlparse, parse_qs
        q = parse_qs(urlparse(directions["href"]).query).get("q", [""])[0]
        address = unquote(q) or None

    postcode = None
    if address:
        m = re.search(r"[A-Z]{1,2}\d[A-Z\d]?\s*\d[A-Z]{2}\b", address, re.IGNORECASE)
        if m:
            postcode = m.group(0).upper()
    return address, postcode


def parse_coordinates(html: str):
    m = re.search(r"center=(-?\d+\.\d+),(-?\d+\.\d+)", html)
    if m:
        return float(m.group(1)), float(m.group(2))
    m = re.search(r"[?&]ll=(-?\d+\.\d+),(-?\d+\.\d+)", html)
    if m:
        return float(m.group(1)), float(m.group(2))
    return None, None


def parse_opening_hours(soup: BeautifulSoup) -> dict:
    hours = {}
    heading = soup.find(
        lambda tag: tag.name in ("h2", "h3") and "Opening Times" in tag.get_text()
    )
    if not heading:
        return hours

    chunk_texts = []
    node = heading
    for _ in range(60):
        node = node.find_next_sibling()
        if node is None:
            break
        text = node.get_text(" ", strip=True)
        if not text:
            continue
        if any(stop in text for stop in ("Facilities", "Download", "Pub history")):
            break
        chunk_texts.append(text)

    joined = " | ".join(chunk_texts)
    for day in DAY_NAMES:
        m = re.search(
            rf"{day}\s*\|?\s*([\d:apm\. ]+(?:-|to|–)[\d:apm\. ]+|Closed)",
            joined,
            re.IGNORECASE,
        )
        if m:
            hours[day] = m.group(1).strip()
    return hours


def parse_facilities(soup: BeautifulSoup) -> list:
    heading = soup.find(
        lambda tag: tag.name in ("h2", "h3") and "Facilities" in tag.get_text()
    )
    if not heading:
        return []
    ul = heading.find_next("ul")
    if not ul:
        return []
    items = [li.get_text(" ", strip=True) for li in ul.find_all("li")]
    return [i for i in items if i]


def parse_history(soup: BeautifulSoup) -> Optional[str]:
    heading = soup.find(
        lambda tag: tag.name in ("h2", "h3") and "Pub history" in tag.get_text()
    )
    if not heading:
        return None
    p = heading.find_next("p")
    return p.get_text(" ", strip=True) if p else None


def parse_photos(soup: BeautifulSoup) -> list:
    photos = []
    for img in soup.find_all("img"):
        src = img.get("src", "")
        if "/wp-content/uploads/" in src and re.search(r"_\d+-\d+x\d+", src):
            photos.append(src)
    seen, unique = set(), []
    for p in photos:
        if p not in seen:
            seen.add(p)
            unique.append(p)
    return unique


def parse_menu_url(soup: BeautifulSoup) -> Optional[str]:
    link = soup.find("a", href=re.compile(r"/pub-menus/"))
    return link["href"] if link else None


def parse_has_hotel(soup: BeautifulSoup) -> bool:
    return soup.find("a", href=re.compile(r"hotels\.jdwetherspoon\.com")) is not None


def parse_pub_file(path: str) -> Pub:
    filename = os.path.basename(path)
    slug = os.path.splitext(filename)[0]
    pub = Pub(source_file=filename, url=slug_to_url(slug))

    try:
        # Read as raw bytes and let BeautifulSoup/UnicodeDammit sort out the
        # encoding -- Edge/Chrome-saved pages are sometimes UTF-8, sometimes
        # Windows-1252 depending on settings, and guessing wrong garbles
        # names with accents or special punctuation (e.g. "Beckett's Bank").
        with open(path, "rb") as f:
            raw = f.read()
        soup = BeautifulSoup(raw, "html.parser")
        html_text = soup.decode()  # normalised text for the regex-based parsers

        pub.name = parse_name(soup)
        pub.phone = parse_phone(soup)
        pub.address, pub.postcode = parse_address_and_postcode(soup)
        pub.latitude, pub.longitude = parse_coordinates(html_text)
        pub.opening_hours = parse_opening_hours(soup)
        pub.facilities = parse_facilities(soup)
        pub.history = parse_history(soup)
        pub.photos = parse_photos(soup)
        pub.menu_url = parse_menu_url(soup)
        pub.has_hotel = parse_has_hotel(soup)
        pub.parsed_ok = bool(pub.name and pub.address)
        if not pub.parsed_ok:
            pub.error = "Missing name or address after parsing - open the file and check its markup"
    except Exception as e:
        pub.error = f"{type(e).__name__}: {e}"

    return pub


# --------------------------------------------------------------------------
# Output: SQLite + CSV + JSON
# --------------------------------------------------------------------------

def build_database(folder: str):
    files = [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.lower().endswith((".htm", ".html"))
    ]
    if not files:
        print(f"No .htm/.html files found in: {folder}")
        sys.exit(1)

    print(f"Found {len(files)} saved page(s) in {folder}")

    pubs = []
    for path in files:
        pub = parse_pub_file(path)
        pubs.append(pub)
        status = "OK" if pub.parsed_ok else f"WARN: {pub.error}"
        print(f"  {pub.source_file}: {pub.name or '???'} -- {status}")

    db_path = os.path.join(folder, "wetherspoon_pubs_local.db")
    csv_path = os.path.join(folder, "wetherspoon_pubs_local.csv")
    json_path = os.path.join(folder, "wetherspoon_pubs_local.json")

    conn = sqlite3.connect(db_path)
    conn.execute("DROP TABLE IF EXISTS pubs")
    conn.execute("""
        CREATE TABLE pubs (
            source_file TEXT PRIMARY KEY,
            url TEXT,
            name TEXT,
            phone TEXT,
            address TEXT,
            postcode TEXT,
            latitude REAL,
            longitude REAL,
            has_hotel INTEGER,
            menu_url TEXT,
            history TEXT,
            facilities TEXT,
            opening_hours TEXT,
            photos TEXT,
            parsed_ok INTEGER,
            error TEXT
        )
    """)
    for pub in pubs:
        conn.execute(
            """
            INSERT INTO pubs (source_file, url, name, phone, address, postcode,
                               latitude, longitude, has_hotel, menu_url, history,
                               facilities, opening_hours, photos, parsed_ok, error)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                pub.source_file, pub.url, pub.name, pub.phone, pub.address,
                pub.postcode, pub.latitude, pub.longitude, int(pub.has_hotel),
                pub.menu_url, pub.history, json.dumps(pub.facilities),
                json.dumps(pub.opening_hours), json.dumps(pub.photos),
                int(pub.parsed_ok), pub.error,
            ),
        )
    conn.commit()

    import csv
    rows = conn.execute("SELECT * FROM pubs ORDER BY name").fetchall()
    cols = [d[0] for d in conn.execute("SELECT * FROM pubs LIMIT 1").description]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(cols)
        writer.writerows(rows)

    records = [dict(zip(cols, row)) for row in rows]
    for r in records:
        for key in ("facilities", "opening_hours", "photos"):
            try:
                r[key] = json.loads(r[key]) if r[key] else ([] if key != "opening_hours" else {})
            except (TypeError, json.JSONDecodeError):
                pass
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

    conn.close()

    ok_count = sum(1 for p in pubs if p.parsed_ok)
    print(f"\nDone. {ok_count}/{len(pubs)} parsed successfully.")
    print(f"  -> {csv_path}")
    print(f"  -> {json_path}")
    print(f"  -> {db_path}")
    if ok_count < len(pubs):
        print("\nSome files didn't parse cleanly (see WARN lines above) -- "
              "open one of those .htm files in a browser and check it looks "
              "like a normal pub page (not a login wall, error page, etc.).")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        folder = sys.argv[1]
    else:
        folder = input("Path to the folder of saved .htm pub pages: ").strip().strip('"')

    if not os.path.isdir(folder):
        print(f"Not a folder: {folder}")
        sys.exit(1)

    build_database(folder)
