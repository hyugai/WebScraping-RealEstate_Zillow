# libs
import os, sys
cwd = os.getcwd()
os.chdir('src'); path_to_src = os.getcwd()
os.chdir(cwd)
if path_to_src not in sys.path:
    sys.path.append(path_to_src)
from _libs import *
from _usr_libs import *

# class URLsScrapper
class URLsScrapper(TableTracker):
    def __init__(self, 
                 db_path: str, table_name: str) -> None:
        super().__init__(db_path, table_name)

# class GeneralScrapper
class GeneralInfoScrapper(TableTracker):
    def __init__(self, 
                 db_path: str, table_name: str, 
                 headers: dict, cities_urls: list[str]) -> None:
        super().__init__(db_path, table_name)
        self.headers = headers
        self.cities_urls = cities_urls
        
    # extract link
    async def pages_hrefs_collector(self, 
                      s: aiohttp.ClientSession, url: str, 
                      queue_hrefs: asyncio.Queue) -> None:
        async with s.get(url) as r:
            content = await r.text() 

            # processing
            dom = etree.HTML(str(BeautifulSoup(content, features='lxml')))
            ancestor_nodes_ul = dom.xpath("//nav[@role='navigation']/child::ul")[0]
            descendant_nodes_a = ancestor_nodes_ul.xpath("./descendant::a[contains(@title, 'Page')]")
            hrefs = [HOMEPAGE_URL + node.get("href") for node in descendant_nodes_a]
            ## processing

            await queue_hrefs.put(hrefs)

    # extract pages links of each city
    async def homes_collector(self,
                              s: aiohttp.ClientSession, 
                              queue_hrefs: asyncio.Queue, queue_homes: asyncio.Queue) -> None:
        while True:
            href = await queue_hrefs.get()
            async with s.get(href) as r:
                content = await r.text()

                # processing

                ## processing
                
                queue_hrefs.task_done()


    async def extract(self):
        queue_hrefs = asyncio.Queue()
        queue_homes = asyncio.Queue()
        async with aiohttp.ClientSession(headers=self.headers) as s:

            await asyncio.run(*[self.func_01(s, url, queue_hrefs) for url in self.cities_urls])

    def transform(self):
        pass

    def load(self):
        pass