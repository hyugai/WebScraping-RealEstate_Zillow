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
db_path = cwd + "/tests/dbs/real_estate.db"
headers = {'Accept-Language': ACCEPT_LANGUAGE, 'Accept-Encoding': ACCEPT_ENCODING, 
           'User-Agent': UserAgent().random} 

ip_tracker = IPTracker(CONTROL_PORT_PASSWD, CONTROL_PORT, PROXIES, headers)
table_tracker = TableTracker(db_path, "city_url")
city_url_scrapper = CityURLScrapper(table_tracker, ip_tracker)
city_url_scrapper.load()
