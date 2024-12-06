# libs
import sys
import json
import sqlite3
import pandas as pd
from pathlib import Path

sys.path.append((Path.cwd()/'src').as_posix())
from extended_scraper import ExtendedScraper

# exp
path_to_db = (Path.cwd()/'tests'/'resource'/'db'/'real_estate.db').as_posix()
with sqlite3.connect(path_to_db) as conn:
    cur = conn.cursor()
    cur.execute("SELECT id, info FROM home")
    rows = [(home_id, json.loads(info)['detailUrl']) for home_id, info in cur.fetchall()]

scraper = ExtendedScraper()
results = scraper.main(rows[:6], 5)

homes = results['home']
with sqlite3.connect(path_to_db) as conn:
    cur = conn.cursor()
    cur.executemany("UPDATE home SET extension=? WHERE id=?", homes)

path_to_failed_home_href = (Path.cwd()/'tests'/'resource'/'db'/'extension'/'failed_detailedHome_href.csv').as_posix()
pd.DataFrame({'href': results['failed_href']}).to_csv(path_to_failed_home_href, index=False)
