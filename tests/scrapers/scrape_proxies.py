# libs
from pathlib import Path
import sys
path_to_src = (Path.cwd() /'src').as_posix()
if path_to_src not in sys.path:
    sys.path.append(path_to_src)
from libs import *

scrape_freeProxyList()
scrape_geonode()
scrape_proxyScrape()