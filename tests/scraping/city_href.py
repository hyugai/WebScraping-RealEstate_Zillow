# libs
import sys
import sqlite3
from pathlib import Path

sys.path.append((Path.cwd()/'src').as_posix())
from city_href_scraper import extract_cities_hrefs

# exp
def scrape():
    cities_hrefs = extract_cities_hrefs()
    path = (Path.cwd()/'tests'/'resource'/'db'/'real_estate.db').as_posix()
    with sqlite3.connect(path) as conn:
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS city_href (href TEXT UNIQUE)')
        cur.executemany('INSERT OR REPLACE INTO city_href VALUES (?)', [(href,) for href in cities_hrefs])
