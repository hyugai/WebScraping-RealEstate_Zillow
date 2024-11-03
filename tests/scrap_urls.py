# libs
import os, sys
cwd = os.getcwd()
os.chdir('src'); path_to_src = os.getcwd()
os.chdir(cwd)
if path_to_src not in sys.path:
    sys.path.append(path_to_src)
from libs import *

# exp: URLScrapper
scrapper = URLScrapper(ZILLOW_HEADERS)
all_hrefs = scrapper.main()

path = cwd + '/tests/db/real_estate.db'
with sqlite3.connect(path) as conn:
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS pages_hrefs (href TEXT UNIQUE)')
    cur.executemany('INSERT OR REPLACE INTO pages_hrefs VALUES (?)', [(href,) for href in all_hrefs['succeeded']])