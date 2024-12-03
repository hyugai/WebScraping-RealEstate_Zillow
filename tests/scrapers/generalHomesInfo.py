# libs
import sys
import pandas as pd
import sqlite3
from pathlib import Path

sys.path.append((Path.cwd()/'src').as_posix())
from zillow import GeneralHomesScraper
ZILLOW_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/wexchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip,deflate,sdch', 'Accept-Language': 'en-US,en;q=0.8', 
    'Referer': 'https://www.google.com.vn'
}

# exp
def scrape():
    db_path = (Path.cwd()/'tests'/'resource'/'db'/'real_estate.db').as_posix()
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM city_href')
        cities_hrefs = [row[0] for row in cur.fetchall()]

    # another exp
    general_homes_scraper = GeneralHomesScraper(ZILLOW_HEADERS)
    results = general_homes_scraper.main(cities_hrefs)

    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS home (id INTEGER UNIQUE, info TEXT, extension TEXT DEFAULT NULL)")
        cur.executemany("INSERT OR REPLACE INTO home (id, info) VALUES (?, ?)", results['home'])

    csv_path = (Path.cwd()/'tests'/'resource'/'db'/'failed_city_href.csv').as_posix()
    pd.DataFrame({'href': results['failed_city_href']})\
        .to_csv(csv_path, index=False)
    csv_path = (Path.cwd()/'tests'/'resource'/'db'/'failed_page_href.csv').as_posix()
    pd.DataFrame({'href': results['failed_page_href']})\
        .to_csv(csv_path, index=False)

def re_scrape():
    pass
