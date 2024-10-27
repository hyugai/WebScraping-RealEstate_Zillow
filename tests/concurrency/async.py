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
urls = [HOMEPAGE_URL]*5
headers = {'Accept-Language': ACCEPT_LANGUAGE, 'Accept-Encoding': ACCEPT_ENCODING, 
            'User-Agent': UserAgent().random}

def non_async_fetch(
    urls: list[str], headers: dict
) -> None:
    for url in urls:
        with requests.Session() as s:
            r = s.get(url, headers=headers)
            if r.status_code != 200:
                print('Failed')
            else:
                print('Succeeded')
                r.text

async def fetch(
    session: aiohttp.ClientSession, url: str
) -> None:
    async with session.get(url) as r:
        if r.status != 200:
            print('Failed')
        else:
            print('Succeeded')
            await r.text()

async def main(
    headers: dict
) -> None:
    queue = asyncio.Queue()
    async with aiohttp.ClientSession(headers=headers) as s:
        tasks = []
        for url in urls:
            tasks.append(fetch(s, url))
        
        await asyncio.gather(*tasks)

start = time.time()
asyncio.run(main(headers=headers))
print(f'Execution time: {time.time() - start}')


start = time.time()
non_async_fetch(urls, headers)
print(f'Execution time: {time.time() - start}')