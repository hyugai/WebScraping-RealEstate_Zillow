# libs
import os, sys
cwd = os.getcwd()
os.chdir('src/'); path_to_src = os.getcwd()
os.chdir(cwd)
from _libs import *
from _usr_libs import *

# exp
db_path = cwd + "/tests/dbs/real_estate.db"
headers = {'User-Agent': USER_AGENTS, 'Accept-Encoding': ACCEPT_ENCODING, 
           'Accept-Language': ACCEPT_LANGUAGE}

home_tracker = TableTracker(db_path, "general_info")
url_tracker = TableTracker(db_path, "city_urls")
home_scrapper = GeneralHomeScrapper_RE(headers, home_tracker, url_tracker)