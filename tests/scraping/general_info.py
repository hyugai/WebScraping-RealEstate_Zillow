# libs
import sys
import pandas as pd
import sqlite3
from pathlib import Path

sys.path.append((Path.cwd()/'src').as_posix())
from general_scraper import GeneralScraper

# exp
def scrape():
    db_path = (Path.cwd()/'tests'/'resource'/'db'/'real_estate.db').as_posix()
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM city_href')
        cities_hrefs = [row[0] for row in cur.fetchall()]

    # another exp
    general_homes_scraper = GeneralScraper()
    results = general_homes_scraper.main(cities_hrefs, 3)

    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS home (id INTEGER UNIQUE, general_info TEXT, detail_url TEXT, extended_info TEXT DEFAULT NULL, is_extended INTEGER DEFAULT 0)")
        cur.executemany("INSERT OR REPLACE INTO home (id, general_info, detail_url) VALUES (?, ?, ?)", results['home'])

    print(results['failed_page_href'])
    csv_path = (Path.cwd()/'tests'/'resource'/'db'/'failed_city_href.csv').as_posix()
    pd.DataFrame({'href': results['failed_city_href']})\
        .to_csv(csv_path, index=False)
    csv_path = (Path.cwd()/'tests'/'resource'/'db'/'failed_page_href.csv').as_posix()
    pd.DataFrame({'href': results['failed_page_href']})\
        .to_csv(csv_path, index=False)

scrape()

def re_scrape():
    pass
