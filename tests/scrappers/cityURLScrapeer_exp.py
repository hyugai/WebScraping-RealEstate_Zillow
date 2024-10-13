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
headers = {'User-Agent': random.choice(USER_AGENTS), 'Accept-Encoding': ACCEPT_ENCODING, 
           'Accept-Language': ACCEPT_LANGUAGE}

table_tracker = TableTracker(db_path, "city_urls")
city_url_scrapper = CityURLScrapper(headers, table_tracker)
city_url_scrapper.extract()
