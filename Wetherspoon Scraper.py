#!/usr/bin/env python3
"""
wetherspoon_scraper.py

Builds a full database/directory of J D Wetherspoon pubs from
www.jdwetherspoon.com.

jdwetherspoon.com's robots.txt (checked 2026-08-03) explicitly permits
crawling and asks for a 10-second delay between requests:

    Crawl-delay: 10
    User-agent: *
    Disallow:
    Sitemap: https://www.jdwetherspoon.com/sitemap_index.xml

This script respects that: every request it makes (sitemap fetches and
pub detail pages alike) is followed by a 10-second pause by default.

WHAT IT DOES
------------
1. DISCOVERY: Fetches the site's own XML sitemap (linked from robots.txt)
   to get a full, authoritative list of every pub's URL
   (https://www.jdwetherspoon.com/pubs/<slug>/) in one or two lightweight
   requests. No browser automation needed -- this is a plain static file
   the site publishes specifically for crawlers.

2. SCRAPING: For every discovered URL, fetches the pub's detail page with
   plain `requests` (these pages are server-rendered, no JS needed) and
   parses out:
     - name
     - phone number
     - full address
     - postcode
     - latitude / longitude (parsed from the embedded map image URL)
     - opening hours for each day of the week
     - facilities / amenities list
     - whether it has an attached hotel
     - pub history blurb
     - photo URLs
     - menu page URL
     - source URL

3. STORAGE: Everything is written to a local SQLite database
   (wetherspoon.db) as it goes, so the script is safely resumable if
   interrupted -- rerun it and it will skip pubs already scraped.
   wetherspoon_pubs.csv / .json are re-exported every few pubs (see
   --export-every) as an atomic, always-consistent snapshot, so you can
   have the CSV open in Excel/Numbers/a text editor and just refresh it
   to watch the directory fill up live while the script keeps running.

USAGE
-----
    pip install requests beautifulsoup4 pandas tqdm

    python wetherspoon_scraper.py                 # discover + scrape everything
    python wetherspoon_scraper.py --skip-discovery # reuse urls already in DB
    python wetherspoon_scraper.py --limit 20       # test on a small batch first

NOTES
-----
- This is a personal-use / research scraper, deliberately paced to match
  the site's own robots.txt Crawl-delay. Please don't turn --delay down
  below 10 seconds.
- Wetherspoon's site markup can change. If a field starts coming back
  empty for most pubs, open one pub page in a browser, view source, and
  adjust the corresponding `parse_*` helper below.
"""

import argparse
import json
import re
import sqlite3
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, asdict, field
from typing import Optional

import requests
from bs4 import BeautifulSoup

try:
    from tqdm import tqdm
except ImportError:  # tqdm is a nice-to-have, not required
    def tqdm(iterable, **kwargs):
        return iterable

BASE_URL = "https://www.jdwetherspoon.com"
PUB_SEARCH_URL = f"{BASE_URL}/pub-search/"
DB_PATH = "wetherspoon.db"
CSV_PATH = "wetherspoon_pubs.csv"
JSON_PATH = "wetherspoon_pubs.json"

USER_AGENT = (
    "Mozilla/5.0 (compatible; WetherspoonDirectoryBot/1.0; "
    "personal research project; contact: set-your-email-here)"
)

DAY_NAMES = [
    "Monday", "Tuesday", "Wednesday", "Thursday",
    "Friday", "Saturday", "Sunday",
]


# --------------------------------------------------------------------------
# Data model
# --------------------------------------------------------------------------

@dataclass
class Pub:
    url: str
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
    scraped_ok: bool = False
    error: Optional[str] = None


# --------------------------------------------------------------------------
# Step 1: discover all pub URLs via the site's own XML sitemap
# --------------------------------------------------------------------------
#
# jdwetherspoon.com's robots.txt (checked 2026-08-03) explicitly allows
# crawling (`Disallow:` is empty) and points to a Yoast-generated sitemap
# index at /sitemap_index.xml, which in turn lists a dedicated
# /pubs-sitemap.xml (and potentially /pubs-sitemap2.xml, etc. if the pub
# count grows past Yoast's per-file cap) containing every pub's URL. This
# is a plain static XML file explicitly published for crawlers, so it
# sidesteps the JS-rendered "Load more" listing page entirely -- no
# headless browser needed for discovery.

SITEMAP_INDEX_URL = f"{BASE_URL}/sitemap_index.xml"
SITEMAP_NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def discover_pub_urls(session: requests.Session, delay: float) -> list:
    """Finds every /pubs/<slug>/ URL via the site's XML sitemaps."""
    import xml.etree.ElementTree as ET

    print(f"Fetching sitemap index: {SITEMAP_INDEX_URL}")
    resp = session.get(SITEMAP_INDEX_URL, timeout=20)
    resp.raise_for_status()
    time.sleep(delay)

    root = ET.fromstring(resp.content)
    sitemap_locs = [
        el.text.strip()
        for el in root.findall("sm:sitemap/sm:loc", SITEMAP_NS)
        if el.text
    ]

    # Only the pub-listing sitemap(s), e.g. pubs-sitemap.xml,
    # pubs-sitemap2.xml -- explicitly excludes pub-histories-sitemap*.xml
    # and pub-menus-sitemap.xml, which point at different page types.
    pub_sitemaps = [u for u in sitemap_locs if re.search(r"/pubs-sitemap\d*\.xml$", u)]
    if not pub_sitemaps:
        print("Could not find a pubs-sitemap*.xml entry in the sitemap index. "
              "Found these sitemaps instead:")
        for u in sitemap_locs:
            print(f"   {u}")
        return []

    urls = set()
    for sm_url in pub_sitemaps:
        print(f"Fetching {sm_url} ...")
        r = session.get(sm_url, timeout=20)
        r.raise_for_status()
        time.sleep(delay)
        sm_root = ET.fromstring(r.content)
        for loc_el in sm_root.findall("sm:url/sm:loc", SITEMAP_NS):
            if loc_el.text:
                loc = loc_el.text.strip()
                if re.match(rf"^{re.escape(BASE_URL)}/pubs/[^/]+/?$", loc):
                    urls.add(loc.rstrip("/") + "/")

    return sorted(urls)


# --------------------------------------------------------------------------
# Step 2: parse a single pub detail page
# --------------------------------------------------------------------------

def fetch_html(url: str, session: requests.Session, timeout: int = 20) -> str:
    resp = session.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp.text


def parse_name(soup: BeautifulSoup) -> Optional[str]:
    h1 = soup.find("h1")
    return h1.get_text(strip=True) if h1 else None


def parse_phone(soup: BeautifulSoup) -> Optional[str]:
    tel = soup.select_one('a[href^="tel:"]')
    if tel:
        return tel.get_text(strip=True) or tel["href"].replace("tel:", "")
    return None


def parse_address_and_postcode(soup: BeautifulSoup):
    """Address text sits right before the 'Get directions' Google Maps link."""
    directions = soup.find("a", href=re.compile(r"maps\.google\.com"))
    address = None
    if directions:
        # The address text is usually the immediately preceding text node(s)
        # within the same parent container.
        parent = directions.find_parent()
        if parent:
            text = parent.get_text(" ", strip=True)
            # Strip the "Get directions to X" link text itself
            text = re.sub(r"Get directions to.*$", "", text).strip()
            address = text or None
    if not address:
        # Fallback: pull it out of the maps query string
        if directions and "q=" in directions["href"]:
            from urllib.parse import unquote, urlparse, parse_qs
            q = parse_qs(urlparse(directions["href"]).query).get("q", [""])[0]
            address = unquote(q) or None

    postcode = None
    if address:
        m = re.search(
            r"[A-Z]{1,2}\d[A-Z\d]?\s*\d[A-Z]{2}\b", address, re.IGNORECASE
        )
        if m:
            postcode = m.group(0).upper()
    return address, postcode


def parse_coordinates(html: str):
    """Coordinates are embedded in the Apple Maps snapshot image URL as
    'center=<lat>,<lng>'. Fall back to any 'q=lat,lng'-style google maps
    param if that's not present."""
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

    # Collect text of the next handful of siblings after the heading and
    # look for "Day  ...  time - time" patterns.
    chunk_texts = []
    node = heading
    for _ in range(60):
        node = node.find_next_sibling()
        if node is None:
            break
        text = node.get_text(" ", strip=True)
        if not text:
            continue
        # Stop once we hit the next major section
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
    # de-dupe, preserve order
    seen = set()
    unique = []
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


def parse_pub_page(url: str, html: str) -> Pub:
    soup = BeautifulSoup(html, "html.parser")
    pub = Pub(url=url)
    try:
        pub.name = parse_name(soup)
        pub.phone = parse_phone(soup)
        pub.address, pub.postcode = parse_address_and_postcode(soup)
        pub.latitude, pub.longitude = parse_coordinates(html)
        pub.opening_hours = parse_opening_hours(soup)
        pub.facilities = parse_facilities(soup)
        pub.history = parse_history(soup)
        pub.photos = parse_photos(soup)
        pub.menu_url = parse_menu_url(soup)
        pub.has_hotel = parse_has_hotel(soup)
        pub.scraped_ok = bool(pub.name and pub.address)
        if not pub.scraped_ok:
            pub.error = "Missing name or address after parsing - check selectors"
    except Exception as e:  # keep going, record the error
        pub.error = f"{type(e).__name__}: {e}"
    return pub


# --------------------------------------------------------------------------
# SQLite storage
# --------------------------------------------------------------------------

def init_db(path: str = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS pubs (
            url TEXT PRIMARY KEY,
            name TEXT,
            phone TEXT,
            address TEXT,
            postcode TEXT,
            latitude REAL,
            longitude REAL,
            has_hotel INTEGER,
            menu_url TEXT,
            history TEXT,
            facilities TEXT,   -- JSON list
            opening_hours TEXT, -- JSON dict
            photos TEXT,       -- JSON list
            scraped_ok INTEGER,
            error TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS discovered_urls (
            url TEXT PRIMARY KEY
        )
    """)
    conn.commit()
    return conn


def save_discovered_urls(conn: sqlite3.Connection, urls: list):
    conn.executemany(
        "INSERT OR IGNORE INTO discovered_urls (url) VALUES (?)",
        [(u,) for u in urls],
    )
    conn.commit()


def load_discovered_urls(conn: sqlite3.Connection) -> list:
    return [r[0] for r in conn.execute("SELECT url FROM discovered_urls")]


def already_scraped_urls(conn: sqlite3.Connection) -> set:
    return {r[0] for r in conn.execute("SELECT url FROM pubs WHERE scraped_ok = 1")}


def save_pub(conn: sqlite3.Connection, pub: Pub):
    conn.execute(
        """
        INSERT INTO pubs (url, name, phone, address, postcode, latitude,
                           longitude, has_hotel, menu_url, history,
                           facilities, opening_hours, photos, scraped_ok, error)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(url) DO UPDATE SET
            name=excluded.name, phone=excluded.phone, address=excluded.address,
            postcode=excluded.postcode, latitude=excluded.latitude,
            longitude=excluded.longitude, has_hotel=excluded.has_hotel,
            menu_url=excluded.menu_url, history=excluded.history,
            facilities=excluded.facilities, opening_hours=excluded.opening_hours,
            photos=excluded.photos, scraped_ok=excluded.scraped_ok, error=excluded.error
        """,
        (
            pub.url, pub.name, pub.phone, pub.address, pub.postcode,
            pub.latitude, pub.longitude, int(pub.has_hotel), pub.menu_url,
            pub.history, json.dumps(pub.facilities), json.dumps(pub.opening_hours),
            json.dumps(pub.photos), int(pub.scraped_ok), pub.error,
        ),
    )
    conn.commit()


def export_csv_json(conn: sqlite3.Connection, quiet: bool = False):
    """Writes the current contents of the DB out to CSV and JSON.

    Written atomically (write to a temp file, then rename into place) so
    that if you have wetherspoon_pubs.csv open in Excel/Numbers/a text
    editor while the scraper is still running, you never see a half
    -written file -- each refresh shows a complete, consistent snapshot.
    """
    import csv
    import os

    rows = conn.execute("SELECT * FROM pubs ORDER BY name").fetchall()
    cols = [d[0] for d in conn.execute("SELECT * FROM pubs LIMIT 1").description]

    tmp_csv = CSV_PATH + ".tmp"
    with open(tmp_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(cols)
        writer.writerows(rows)
    os.replace(tmp_csv, CSV_PATH)

    records = [dict(zip(cols, row)) for row in rows]
    for r in records:
        for key in ("facilities", "opening_hours", "photos"):
            try:
                r[key] = json.loads(r[key]) if r[key] else ([] if key != "opening_hours" else {})
            except (TypeError, json.JSONDecodeError):
                pass
    tmp_json = JSON_PATH + ".tmp"
    with open(tmp_json, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)
    os.replace(tmp_json, JSON_PATH)

    if not quiet:
        print(f"Exported {len(rows)} pubs -> {CSV_PATH}, {JSON_PATH}")


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def scrape_one(url: str, session: requests.Session, delay: float) -> Pub:
    try:
        html = fetch_html(url, session)
        pub = parse_pub_page(url, html)
    except Exception as e:
        pub = Pub(url=url, error=f"{type(e).__name__}: {e}")
    time.sleep(delay)
    return pub


def main():
    parser = argparse.ArgumentParser(description="Scrape the full J D Wetherspoon pub directory.")
    parser.add_argument("--skip-discovery", action="store_true",
                         help="Reuse pub URLs already stored in the database instead of "
                              "re-fetching the sitemap.")
    parser.add_argument("--workers", type=int, default=1,
                         help="Number of concurrent detail-page requests. "
                              "jdwetherspoon.com's robots.txt asks for a 10-second "
                              "crawl-delay, which this script applies per request, so "
                              "keep this at 1 unless you've deliberately chosen to "
                              "spread that delay across parallel workers instead "
                              "(--workers N with --delay N*10 keeps the same overall rate).")
    parser.add_argument("--delay", type=float, default=10.0,
                         help="Seconds to sleep after each request (sitemap fetches and "
                              "pub pages alike). Default 10, matching the Crawl-delay "
                              "directive in jdwetherspoon.com's robots.txt -- please "
                              "don't set this lower.")
    parser.add_argument("--limit", type=int, default=None,
                         help="Optional cap on number of pubs to scrape (useful for testing).")
    parser.add_argument("--export-every", type=int, default=5,
                         help="Re-write the CSV/JSON export after every N pubs scraped, "
                              "so you can open wetherspoon_pubs.csv and watch it fill up "
                              "live while the script keeps running. Set to 1 to export "
                              "after every single pub. Default 5.")
    args = parser.parse_args()

    conn = init_db()
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})

    if args.skip_discovery:
        urls = load_discovered_urls(conn)
        if not urls:
            print("No URLs stored yet -- run without --skip-discovery first.")
            sys.exit(1)
    else:
        print("Discovering pub URLs via the site's XML sitemap...")
        urls = discover_pub_urls(session, delay=args.delay)
        print(f"Discovered {len(urls)} pub URLs.")
        if not urls:
            print("\nNo pub URLs were found in the sitemap. Double check "
                  f"{SITEMAP_INDEX_URL} still lists a pubs-sitemap*.xml entry "
                  "(the site's structure may have changed).")
            conn.close()
            sys.exit(1)
        save_discovered_urls(conn, urls)

    done = already_scraped_urls(conn)
    todo = [u for u in urls if u not in done]
    if args.limit:
        todo = todo[: args.limit]

    print(f"{len(done)} already scraped, {len(todo)} remaining.")

    # Export whatever's already in the DB immediately, so the CSV/JSON files
    # exist and are openable right from the start (useful if resuming a
    # previous run -- you don't have to wait for the first new pub).
    export_csv_json(conn)

    scraped_since_export = 0
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(scrape_one, url, session, args.delay): url
            for url in todo
        }
        for future in tqdm(as_completed(futures), total=len(futures), desc="Scraping pubs"):
            pub = future.result()
            save_pub(conn, pub)
            if not pub.scraped_ok:
                print(f"  [warn] {pub.url} -> {pub.error}")

            scraped_since_export += 1
            if scraped_since_export >= args.export_every:
                export_csv_json(conn, quiet=True)
                scraped_since_export = 0

    # Final export to make sure the very last batch is included
    export_csv_json(conn)
    conn.close()


if __name__ == "__main__":
    main()
