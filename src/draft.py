# libs
import os, sys
cwd = os.getcwd()
os.chdir('src'); path_to_src = os.getcwd()
os.chdir(cwd)
if path_to_src not in sys.path:
    sys.path.append(path_to_src)
from _libs import *
from _usr_libs import *

# class GeneralScrapper
class GeneralScrapper(TableTracker):
    def __init__(self, 
                 db_path: str, table_name: str, 
                 headers: dict, cities_urls: list[str]
) -> None:
        super().__init__(db_path, table_name)
        self.headers = headers
        self.cities_urls = cities_urls