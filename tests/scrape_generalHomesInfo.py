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
    cur.execute('SELECT * FROM pages_hrefs')
    pages_hrefs = [row[0] for row in cur.fetchall()]
    
home_scraper = GeneralHomeScraper(ZILLOW_HEADERS, pages_hrefs)
home_scraper.main()