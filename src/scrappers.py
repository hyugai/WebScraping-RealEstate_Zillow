# libs
from libs import *
from aiohttp_socks.connector import ProxyConnector

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
                                s: aiohttp.ClientSession, city_href: str, 
                                queue: asyncio.Queue):
        self.headers['User-Agent'] = UserAgent().random
        async with s.get(city_href, headers=self.headers) as r:
            if (r.status == 200): 
                content = await r.text()

                dom = etree.HTML(str(BeautifulSoup(content, features='lxml')))
                xpath = "//li[contains(@class, 'PaginationNumberItem')]/child::a"
                nodes_a = dom.xpath(xpath)
                
                if len(nodes_a) != 0:
                    pages_hrefs = [ZILLOW + node.get('href') for node in nodes_a]

                    await queue.put(pages_hrefs)
                    queue.task_done()
            else:
                print(city_href)

    async def extract(self, 
                      hrefs: list[str]):
        queue = asyncio.Queue()
        async with aiohttp.ClientSession(headers={'Referer': ZILLOW}) as s:
            tasks = [self.pages_collector(s, href, queue) for href in hrefs] 
            
            await asyncio.gather(*tasks)

            await queue.join()
    
    def retry(self):
        pass

    def main(self):
        hrefs = self.cities_collector()
        asyncio.run(self.extract(hrefs))