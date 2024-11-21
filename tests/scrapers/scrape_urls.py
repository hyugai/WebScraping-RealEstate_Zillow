# libs
from pathlib import Path
import sys

path_to_src = (Path.cwd()/'src').as_posix()
if path_to_src not in sys.path:
    sys.path.append(path_to_src)
from usr_libs import *

cities_hrefs = extract_cities_hrefs(ZILLOW_HEADERS)
path = (Path.cwd()/'tests'/'resource'/'db'/'real_estate.db').as_posix()
with sqlite3.connect(path) as conn:
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS city_href (href TEXT UNIQUE)')
    cur.executemany('INSERT OR REPLACE INTO city_href VALUES (?)', [(href,) for href in cities_hrefs])