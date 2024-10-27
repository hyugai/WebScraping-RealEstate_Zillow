# libs
import os, sys
cwd = os.getcwd()
os.chdir('src'); path_to_src = os.getcwd()
os.chdir(cwd)
if path_to_src not in sys.path:
    sys.path.append(path_to_src)
from _libs import *
from _usr_libs import *
from aiohttp_socks import ProxyConnector

# exp
urls = [HOMEPAGE_URL]*5

async def fetch(
    session: aiohttp.ClientSession, url: str
) -> None:
    async with session.get(url) as r:
        print(r.status)
        await r.text()

async def main() -> None:
    queue = asyncio.Queue()
    headers = {'Accept-Language': ACCEPT_LANGUAGE, 'Accept-Encoding': ACCEPT_ENCODING, 
                'User-Agent': UserAgent().random}
    async with aiohttp.ClientSession(headers=headers) as s:
        tasks = []
        for url in urls:
            tasks.append(fetch(s, url))
        
        await asyncio.gather(*tasks)

asyncio.run(main())