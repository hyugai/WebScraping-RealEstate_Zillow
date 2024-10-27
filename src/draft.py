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
class GeneralInfoScrapper(TableTracker):
    def __init__(self, 
                 db_path: str, table_name: str, 
                 headers: dict, cities_urls: list[str]) -> None:
        super().__init__(db_path, table_name)
        self.headers = headers
        self.cities_urls = cities_urls
        
    async def func_01(self, 
                      s: aiohttp.ClientSession, url: str, 
                      queue: asyncio.Queue) -> None:
        async with s.get(url) as r:
            content = await r.text() 
            await queue.put(content)

    async def func_02(self):
        pass

    async def test(self):
        queue = asyncio.Queue()
        async with aiohttp.ClientSession(headers=self.headers) as s:

            await asyncio.run(*[self.func_01(s, url, queue) for url in self.cities_urls])

    def extract(self):
        pass

    def transform(self):
        pass

    def load(self):
        pass