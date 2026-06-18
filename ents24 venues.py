"""
ents24_venues.py
----------------
Scrapes every venue listed on ents24.com/venues and saves to CSV.

Output: ents24_venues.csv
Fields: name, city, url, prefix

Run: python ents24_venues.py
Requires: pip install requests beautifulsoup4
"""

import requests
import csv
import time
import re
from bs4 import BeautifulSoup

OUTPUT_CSV    = "ents24_venues.csv"
BASE_URL      = "https://www.ents24.com"
DELAY_SECONDS = 0.5

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept":     "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-GB,en;q=0.9",
}

# All prefixes from the index page
PREFIXES = [
    "#", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
    "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
]


def fetch_page(url):
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")


def parse_venues(soup):
    """Extract venue name, city and URL from a listing page."""
    venues = []
    # Venues are in <ul> list items as links — find the main content list
    for li in soup.select("ul li a"):
        href = li.get("href", "")
        text = li.get_text(strip=True)
        # Venue links follow pattern /city-events/venue-slug
        if "-events/" in href and href.startswith("/"):
            # Extract city from URL: /birmingham-events/venue -> Birmingham
            match = re.match(r"/([^/]+)-events/", href)
            city  = match.group(1).replace("-", " ").title() if match else ""
            # Name and city are in the text as "Venue Name, City"
            if ", " in text:
                name = text.rsplit(", ", 1)[0]
                city = text.rsplit(", ", 1)[1]
            else:
                name = text
            venues.append({
                "name": name,
                "city": city,
                "url":  BASE_URL + href,
            })
    return venues


def get_next_page_url(soup):
    """Return the URL of the next page if it exists."""
    next_link = soup.find("a", string=re.compile(r"Next page", re.I))
    if next_link and next_link.get("href"):
        href = next_link["href"]
        return href if href.startswith("http") else BASE_URL + href
    return None


def scrape_prefix(prefix):
    """Scrape all pages for a given prefix letter."""
    encoded = "%23" if prefix == "#" else prefix
    url     = f"{BASE_URL}/venues?prefix={encoded}"
    venues  = []
    page    = 1

    while url:
        try:
            soup = fetch_page(url)
        except Exception as e:
            print(f"    ✗ Error fetching {url}: {e}")
            break

        page_venues = parse_venues(soup)
        venues.extend(page_venues)
        next_url = get_next_page_url(soup)

        print(f"    Prefix '{prefix}' page {page}: {len(page_venues)} venues", end="")
        if next_url:
            print(f" → next page")
        else:
            print(f" (done)")

        url   = next_url
        page += 1
        if next_url:
            time.sleep(DELAY_SECONDS)

    return venues


def main():
    print("▶ Scraping all UK venues from Ents24...\n")

    all_venues = []

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["name", "city", "url", "prefix"])
        writer.writeheader()

        for prefix in PREFIXES:
            print(f"  Letter: '{prefix.upper()}'")
            venues = scrape_prefix(prefix)

            for v in venues:
                v["prefix"] = prefix
                writer.writerow(v)
            csvfile.flush()

            all_venues.extend(venues)
            print(f"  → {len(venues)} venues for '{prefix.upper()}' "
                  f"| Running total: {len(all_venues)}\n")
            time.sleep(DELAY_SECONDS)

    print(f"✓ Complete! {len(all_venues)} venues saved to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
