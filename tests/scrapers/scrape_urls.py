# libs
import os, sys
cwd = os.getcwd()
os.chdir('src'); path_to_src = os.getcwd()
os.chdir(cwd)
if path_to_src not in sys.path:
    sys.path.append(path_to_src)
from libs import *

cities_hrefs = extract_cities_hrefs(ZILLOW_HEADERS)
path = cwd + '/tests/resource/db/real_estate.db'
with sqlite3.connect(path) as conn:
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS city_href (href TEXT UNIQUE)')
    cur.executemany('INSERT OR REPLACE INTO city_href VALUES (?)', [(href,) for href in cities_hrefs])