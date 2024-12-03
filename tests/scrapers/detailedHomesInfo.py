# libs
from pathlib import Path
from sqlite3 import sqlite_version
import sys

path_to_src = (Path.cwd()/'src').as_posix()
if path_to_src not in sys.path:
    sys.path.append(path_to_src)
from usr_libs import *

# exp
path_to_db = (Path.cwd()/'tests'/'resource'/'db'/'real_estate.db').as_posix()
with sqlite3.connect(path_to_db) as conn:
    cur = conn.cursor()
    cur.execute("SELECT id, info FROM home")
    rows = [(id, json.loads(info)['detailUrl']) for id, info in cur.fetchall()]
