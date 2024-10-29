# libs
from libs import *

# URLsCollector
class URLScrapper(TableTracker):
    def __init__(self,
                 path: str, name: str, 
                 headers: dict):
        super().__init__(path, name)
        self.headers = headers

    def cities_collector(self) -> list[str]:
        with requests.Session() as s:
            self.headers['User-Agent'] = UserAgent().random 
            r = s.get(ZILLOW, headers=self.headers) 

            if r.status_code == 200:
                dom = etree.HTML(str(BeautifulSoup(r.text, features='lxml'))) 
                xpath = "//button[text()='Real Estate']/parent::div/following-sibling::ul/child::li/descendant::a"
                nodes_a = dom.xpath(xpath)
                full_hrefs = [ZILLOW + node.get('href') for node in nodes_a]

                return full_hrefs
            else:
                raise ValueError(f'Failed fetching (error code: {r.status_code})')

    async def pages_collector(self,
                                s: aiohttp.ClientSession, href: str, 
                                queue: asyncio.Queue):
        async with s.get(href) as r:
            if r.status == 200:
                content = await r.text()
            else:
                print(r.status)

    async def main_extract(self):
        hrefs = self.cities_collector()

        self.headers['User-Agent'] = UserAgent().random
        queue = asyncio.Queue()
        async with aiohttp.ClientSession(headers=self.headers) as s:
            tasks = [self.pages_collector(s, href, queue) for href in hrefs] 
            
            await asyncio.gather(*tasks)
    
    def main(self):
        asyncio.run(self.main_extract())