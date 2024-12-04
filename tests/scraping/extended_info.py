# libs
import sys
import json
import asyncio
import sqlite3
from pathlib import Path

sys.path.append((Path.cwd()/'src').as_posix())
from extended_scraper import ExtendedScraper

# exp
path_to_db = (Path.cwd()/'tests'/'resource'/'db'/'real_estate.db').as_posix()
with sqlite3.connect(path_to_db) as conn:
    cur = conn.cursor()
    cur.execute("SELECT id, info FROM home")
    rows = [(id, json.loads(info)['detailUrl']) for id, info in cur.fetchall()]
    
queue_href = asyncio.Queue()
[queue_href.put_nowait(i) for i in rows[:6]]
print(rows[:6])

scraper = ExtendedScraper()
results = asyncio.run(scraper.collect(queue_href))
print(results)
