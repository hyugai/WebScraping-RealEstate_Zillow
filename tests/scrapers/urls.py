# libs
import sys
import sqlite3
from pathlib import Path

sys.path.append((Path.cwd()/'src').as_posix())
from zillow import extract_cities_hrefs

ZILLOW_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/wexchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip,deflate,sdch', 'Accept-Language': 'en-US,en;q=0.8', 
    'Referer': 'https://www.google.com.vn'
}

# exp
def scrape():
    cities_hrefs = extract_cities_hrefs(ZILLOW_HEADERS)
    path = (Path.cwd()/'tests'/'resource'/'db'/'real_estate.db').as_posix()
    with sqlite3.connect(path) as conn:
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS city_href (href TEXT UNIQUE)')
        cur.executemany('INSERT OR REPLACE INTO city_href VALUES (?)', [(href,) for href in cities_hrefs])
