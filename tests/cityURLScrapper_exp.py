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
db_path = cwd + "tests/dbs/homes_by_city.db"

zillow = ZillowHeadlessBrowser()
url_tracker = TableTracker(db_path, "urls")
city_url_scrapper = CityURLScrapper(zillow, url_tracker)
city_url_scrapper.extract()
