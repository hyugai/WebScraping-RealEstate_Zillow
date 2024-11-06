import sys
from pathlib import Path
path_to_src = (Path.cwd()/'src').as_posix()
if path_to_src not in sys.path:
    sys.path.append(path_to_src) 
from libs import * 

# exp
#scrape_freeProxyList()
#csv_path = (Path.cwd()/'tests'/'resource'/'proxies'/'free_proxy_list.csv').as_posix()
#df_proxies = pd.read_csv(csv_path)
#proxies_pool = [f"http://{ip}:{port}" for ip, port in zip(df_proxies['ip_address'], df_proxies['port'])]    
#
#async def fetch_url():
#    async with aiohttp.ClientSession(headers={'Referer': 'https://www.google.com.vn'}) as s:
#        while True:
#            try:
#                headers = ZILLOW_HEADERS
#                headers['User-Agent'] = UserAgent().random
#                async with s.get('https://www.zillow.com/albuquerque-nm/', headers=headers, proxy=random.choice(proxies_pool)) as r:
#                    if r.status == 200:
#                        content = await r.text()
#                        print(BeautifulSoup(content, features='lxml').prettify())
#
#                        break
#                    else:
#                        continue
#            except Exception:
#                continue 
#
#asyncio.run(fetch_url())

with open('test.txt', 'r') as f:
    text = f.read()

text = json.loads(text)