import sys
from pathlib import Path

import aiohttp.client_exceptions
path_to_src = (Path.cwd()/'src').as_posix()
if path_to_src not in sys.path:
    sys.path.append(path_to_src) 
from libs import * 

#exp
def scrap_1Page():
    scrape_freeProxyList()
    csv_path = (Path.cwd()/'tests'/'resource'/'proxies'/'free_proxy_list.csv').as_posix()
    df_proxies = pd.read_csv(csv_path)
    proxies_pool = [f"http://{ip}:{port}" for ip, port in zip(df_proxies['ip_address'], df_proxies['port'])]    

    async def fetch_url():
        async with aiohttp.ClientSession(headers={'Referer': 'https://www.google.com.vn'}, connector=aiohttp.TCPConnector()) as s:
            while True:
                try:
                    headers = ZILLOW_HEADERS
                    headers['User-Agent'] = UserAgent().random
                    proxy = random.choice(proxies_pool)
                    async with s.get('https://www.zillow.com/albuquerque-nm/', headers=headers, proxy=proxy) as r:
                        if r.status == 200:
                            print('OK')

                            break
                        else:
                            continue
                except Exception as e:
                    print(e, proxy)

    asyncio.run(fetch_url())

def handle_string():
    with open('test.txt', 'r') as f:
        text = f.read()

    text: dict = json.loads(text)
    key_to_find = 'listResults'
    while key_to_find not in text:
        tmp_dict = {}
        [tmp_dict.update(value) for value in text.values() if isinstance(value, dict)]
        text = tmp_dict 

    homes_info = text[key_to_find]
    pd.json_normalize(homes_info).to_csv('fee.csv', index=False)
    
handle_string()