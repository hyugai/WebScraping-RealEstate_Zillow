# libs
import os, sys
cwd = os.getcwd()
os.chdir('src/'); path_to_src = os.getcwd()
os.chdir(cwd)
if path_to_src not in sys.path:
    sys.path.append(path_to_src)
from _libs import *
from _usr_libs import *

# exp
with sqlite3.connect('tests/dbs/real_estate.db') as conn:
    pd.read_sql("select * from city_url", conn).to_csv('test.csv', index=False)