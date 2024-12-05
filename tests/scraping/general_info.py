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
    results = general_homes_scraper.main(cities_hrefs)

#    with sqlite3.connect(db_path) as conn:
#        cur = conn.cursor()
#        cur.execute("CREATE TABLE IF NOT EXISTS home (id INTEGER UNIQUE, info TEXT, extension TEXT DEFAULT NULL)")
#        cur.executemany("INSERT OR REPLACE INTO home (id, info) VALUES (?, ?)", results['home'])
#
#    csv_path = (Path.cwd()/'tests'/'resource'/'db'/'general'/'failed_city_href.csv').as_posix()
#    pd.DataFrame({'href': results['failed_city_href']})\
#        .to_csv(csv_path, index=False)
#    csv_path = (Path.cwd()/'tests'/'resource'/'db'/'general'/'failed_page_href.csv').as_posix()
#    pd.DataFrame({'href': results['failed_page_href']})\
#        .to_csv(csv_path, index=False)

scrape()

def re_scrape():
    pass
