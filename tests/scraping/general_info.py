# libs
import sys
import pandas as pd
import sqlite3
from pathlib import Path

sys.path.append((Path.cwd()/'src').as_posix())
from general_scraper import GeneralScraper


db_path = (Path.cwd()/'tests'/'resource'/'db'/'real_estate.db').as_posix()
with sqlite3.connect(db_path) as conn:
    cur = conn.cursor()
    cur.execute('SELECT * FROM city_href')
    cityHref_throughDB = [row[0] for row in cur.fetchall()]

csv_path = (Path.cwd()/'tests'/'resource'/'failed_page_href.csv').as_posix() 
failed_pageHref = pd.read_csv(csv_path)['href'].values.tolist()

csv_path - (Path.cwd()/'tests'/'resource'/'failed_page_href.csv').as_posix()
failed_cityHref = pd.read_csv(csv_path)['href'].values.tolist()

# exp
def scrape():
    # another exp
    general_homes_scraper = GeneralScraper()
    results = general_homes_scraper.main(cityHref_throughDB, 3)

    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS home (id INTEGER UNIQUE, general_info TEXT, detail_url TEXT, extended_info TEXT DEFAULT NULL, is_extended INTEGER DEFAULT 0)")
        # cur.executemany("INSERT OR IGNORE INTO home (id, general_info, detail_url) VALUES (?, ?, ?)", results['home']) # use IGNORE to preserve the information

        # this query is used to update the general_info column if id has already existed but the general_info is updated from the web
        cur.executemany("INSERT INTO home(id, general_info, detail_url) VALUES(?, ?, ?) \
                            ON CONFLICT (id) \
                            DO \
                                UPDATE \
                                SET general_info=excluded.general_info \
                                WHERE home.general_info != excluded.general_info") # update genral_info if its old info is different from the new one

    csv_path = (Path.cwd()/'tests'/'resource'/'db'/'failed_city_href.csv').as_posix()
    pd.DataFrame({'href': results['failed_city_href']})\
        .to_csv(csv_path, index=False)
    csv_path = (Path.cwd()/'tests'/'resource'/'db'/'failed_page_href.csv').as_posix()
    pd.DataFrame({'href': results['failed_page_href']})\
        .to_csv(csv_path, index=False)

def re_scrapeHome_throughFailedPageHref():
    scraper = GeneralScraper()
    results = scraper.collectHomes_throughPageHref(failed_pageHref, 3)

    db_path = (Path.cwd()/'tests'/'resource'/'real_estate.db').as_posix()
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.executemany("INSERT INTO home(id, general_info, detail_url) VALUES(?, ?, ?)\
                        ON CONFLICT(id)\
                        DO\
                            UPDATE\
                            SET general_info=excluded.general_info\
                            WHERE home.general_info != excluded.general_info", results)

