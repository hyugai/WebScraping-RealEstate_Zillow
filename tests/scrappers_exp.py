# libs
import os, sys
cwd = os.getcwd()
os.chdir('src'); path_to_src = os.getcwd()
os.chdir(cwd)
if path_to_src not in sys.path:
    sys.path.append(path_to_src)
from libs import *

# exp: URLScrapper
def url_scrapper():
    path = cwd + 'db/real_estate.db'
    name = 'city_url'
    scrapper = URLScrapper(path, name, ZILLOW_HEADERS)
    scrapper.main()

url_scrapper()