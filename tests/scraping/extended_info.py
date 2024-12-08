# libs
import sys
import sqlite3
from pathlib import Path

sys.path.append((Path.cwd()/'src').as_posix())
from extended_scraper import ExtendedScraper

# exp
def scrape():
    path_to_db = (Path.cwd()/'tests'/'resource'/'db'/'real_estate.db').as_posix()
    with sqlite3.connect(path_to_db) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, detail_url FROM home WHERE is_extended = 0")
        rows = cur.fetchall()

    scraper = ExtendedScraper()
    results = scraper.main(rows, 3)

    homes = results['home']
    if homes:
        with sqlite3.connect(path_to_db) as conn:
            cur = conn.cursor()
            cur.executemany("UPDATE home SET extended_info=?, is_extended=? WHERE id=?", homes)
