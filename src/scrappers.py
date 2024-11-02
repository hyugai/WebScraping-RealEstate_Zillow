# libs
from libs import *

# URLsCollector
class URLScrapper(TableTracker):
    def __init__(self,
                 path: str, name: str, 
                 headers: dict[str, str]):
        super().__init__(path, name)
        self.headers = headers

    def extract_cities_hrefs(self) -> list[str]:
        with requests.Session() as s:
            self.headers['User-Agent'] = UserAgent().random 
            r = s.get(ZILLOW, headers=self.headers) 

            if r.status_code == 200:
                dom = etree.HTML(str(BeautifulSoup(r.text, features='lxml'))) 
                xpath = "//button[text()='Real Estate']/parent::div/following-sibling::ul/child::li/descendant::a"
                nodes_a = dom.xpath(xpath)
                full_hrefs = [ZILLOW + node.get('href') for node in nodes_a if node.get('href') != '/browse/homes/']

                return full_hrefs
            else:
                raise ValueError(f'Failed fetching (error code: {r.status_code})')

    async def extract_pages_hrefs(self,
                                s: aiohttp.ClientSession, city_href: str, 
                                queues: dict[str, asyncio.Queue]):
        self.headers['User-Agent'] = UserAgent().random
        async with s.get(city_href, headers=self.headers) as r:
            if (r.status == 200): 
                content = await r.text()

                dom = etree.HTML(str(BeautifulSoup(content, features='lxml')))
                xpath = "//li[contains(@class, 'PaginationNumberItem')]/child::a"
                nodes_a = dom.xpath(xpath)
                
                pages_hrefs = [ZILLOW + node.get('href') for node in nodes_a]
                for href in pages_hrefs:
                    await queues['succeeded'].put(href)
            else:
                await queues['retry'].put(city_href) 

    async def collect(self, 
                      hrefs: list[str]) -> dict[str, asyncio.Queue]:
        queues = {'succeeded': asyncio.Queue(), 'retry': asyncio.Queue()}
        async with aiohttp.ClientSession(headers={'Referer': ZILLOW}) as s:
            tasks_pages_collector = [asyncio.create_task(self.extract_pages_hrefs(s, href, queues)) for href in hrefs]

            await asyncio.gather(*tasks_pages_collector)

            # print out results
            print(f"Succeeded: {queues['succeeded'].qsize()}\nFailed: {queues['retry'].qsize()}")
            ##
        
        return queues
    
    def main(self):
        hrefs = self.extract_cities_hrefs()
        queues = asyncio.run(self.collect(hrefs))

    def retry(self):
        pass


class GeneralHomeExtractor():
    def __init__(self, 
                 headers: dict[str, str], pages_hrefs: list[str]) -> None:
        self.headers = headers
        self.pages_hrefs = pages_hrefs

    async def homes_extractor(self, 
                              s: aiohttp.ClientSession, queue: asyncio.Queue, 
                              href: str):
        self.headers['User-Agent'] = UserAgent().random
        async with s.get(href, headers=self.headers) as r:
            if (r.status == 200):
                content = await r.text() 

                dom = etree.HTML(str(BeautifulSoup(content, features='lxml')))
                xpath = "//script[@type='application/json']"
                nodes_script = dom.xpath(xpath)
                print(len(nodes_script))
            else:
                print('Failed') 

    async def collect(self):
        pass