# libs
import sys
from pathlib import Path

src_path = (Path.cwd()/'src').as_posix()
if src_path not in sys.path:
    sys.path.append(src_path)
from libs import *

# exp
db_path = (Path.cwd()/'tests'/'resource'/'db'/'real_estate.db').as_posix()
with sqlite3.connect(db_path) as conn:
    cur = conn.cursor()
    cur.execute('SELECT * FROM city_href')
    cities_hrefs = [row[0] for row in cur.fetchall()]

#scrape_freeProxyList()
#csv_path = (Path.cwd()/'tests'/'resource'/'proxies'/'free_proxy_list.csv').as_posix()
#df_proxies = pd.read_csv(csv_path)
#proxies_pool = [f"http://{ip}:{port}" for ip, port in zip(df_proxies['ip_address'], df_proxies['port'])]    
#
#scrape_geonode()
#csv_path = (Path.cwd()/'tests'/'resource'/'proxies'/'free_proxy_list.csv').as_posix()
#df_proxies = pd.read_csv(csv_path)

#home_scraper = GeneralHomeScraper(ZILLOW_HEADERS, proxies_pool)
#collecteHomes, hrefsToRetry = home_scraper.main(pages_hrefs)
#
#db_path = (Path.cwd()/'tests'/'resource'/'db'/'real_estate.db').as_posix()
#with sqlite3.connect(db_path) as conn:
#    cur = conn.cursor()
#    cur.execute('CREATE TABLE IF NOT EXISTS homes_as_json (id INTEGER UNIQUE, json TEXT)')
#    cur.executemany('INSERT OR REPLACE INTO homes_as_json (id, json) VALUES (?, ?)', collecteHomes)
#
#csv_path = (Path.cwd()/'tests'/'resource'/'db'/'hrefsToRetry.csv').as_posix()
#pd.DataFrame({'href': hrefsToRetry}).to_csv(csv_path, index=False)

# another exp
general_homes_scraper = TestGeneralHomesScraper(ZILLOW_HEADERS)
results = general_homes_scraper.main(cities_hrefs)

with sqlite3.connect(db_path) as conn:
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS home (id TEXT UNIQUE, json TEXT)")
    cur.executemany("INSERT OR REPLACE INTO home (id, json) VALUES (?, ?)", results['home'])

csv_path = (Path.cwd()/'tests'/'resource'/'db'/'failed_city_href.csv').as_posix()
pd.DataFrame({'href': results['failed_city_href']})\
    .to_csv(csv_path, index=False)
csv_path = (Path.cwd()/'tests'/'resource'/'db'/'failed_page_href.csv').as_posix()
pd.DataFrame({'href': results['failed_page_href']})\
    .to_csv(csv_path, index=False)