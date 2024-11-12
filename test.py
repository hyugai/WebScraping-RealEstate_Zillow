import sys
from pathlib import Path

path_to_src = (Path.cwd()/'src').as_posix()
if path_to_src not in sys.path:
    sys.path.append(path_to_src) 
from libs import * 

#exp
db_path = (Path.cwd()/'tests'/'resource'/'db'/'real_estate.db').as_posix()
with sqlite3.connect(db_path) as conn:
    cur = conn.cursor()
    cur.execute("select * from home")
    rows = cur.fetchall()
    print(rows[0])
