# libs
import sys
from pathlib import Path

src_path = (Path.cwd()/'src').as_posix()
if src_path not in sys.path:
    sys.path.append(src_path)
from libs import *

# exp
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
    cur.execute("CREATE TABLE IF NOT EXISTS home (id TEXT UNIQUE, json TEXT)")
    cur.executemany("INSERT OR REPLACE INTO home (id, json) VALUES (?, ?)", results['home'])

csv_path = (Path.cwd()/'tests'/'resource'/'db'/'failed_city_href.csv').as_posix()
pd.DataFrame({'href': results['failed_city_href']})\
    .to_csv(csv_path, index=False)
csv_path = (Path.cwd()/'tests'/'resource'/'db'/'failed_page_href.csv').as_posix()
pd.DataFrame({'href': results['failed_page_href']})\
    .to_csv(csv_path, index=False)