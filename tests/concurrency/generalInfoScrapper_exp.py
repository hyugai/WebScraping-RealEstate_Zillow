# libs
import os, sys
cwd = os.getcwd()
os.chdir('src'); path_to_src = os.getcwd()
os.chdir(cwd)
if path_to_src not in sys.path:
    sys.path.append(path_to_src)
from _libs import *
from _usr_libs import *

# exp
def exp() -> None:
    db_path = cwd + "/src/dbs/real_estate.db"
    table_name = "async"
    headers = {'Accept-Language': ACCEPT_LANGUAGE, 'Accept-Encoding': ACCEPT_ENCODING, 
               'User-Agent': UserAgent().random}
    

    scrapper = GeneralInfoScrapper(db_path, table_name, headers)