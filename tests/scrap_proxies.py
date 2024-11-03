# libs
from pathlib import Path
import sys
path_to_src = (Path.cwd() / 'src').as_posix()
if path_to_src not in sys.path:
    sys.path.append(path_to_src)
from libs import *

# exp: https://free-proxy-list.net/
def scrap_free_proxy_list():
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/wexchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip,deflate,sdch', 'Accept-Language': 'en-US,en;q=0.8',
            'Referer': 'https://www.google.com', 'Connection': 'keep-alive'}
    csv_path = (Path.cwd()/'tests'/'resource'/'proxies'/'free_proxy_list.csv').as_posix()

    scraper = FreeProxyListScraper(headers, csv_path) 
    scraper.load()