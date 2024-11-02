# libs
from libs import *

# URLsCollector
class URLScrapper(TableTracker):
    def __init__(self,
                 path: str, name: str, 
                 headers: dict[str, str]):
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
                full_hrefs = [ZILLOW + node.get('href') for node in nodes_a if node.get('href') != '/browse/homes/']

                return full_hrefs
            else:
                raise ValueError(f'Failed fetching (error code: {r.status_code})')

    async def pages_collector(self,
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
                await queues['succeeded'].put(pages_hrefs)
                #queues['succeeded'].task_done()
            else:
                await queues['retry'].put(city_href) 
                #queues['retry'].task_done()
    
    async def homes_collector(self, 
                              s: aiohttp.ClientSession, queue: asyncio.Queue, 
                              tasks_pages_collector: list[asyncio.Task]):
        count = 1
        flag = [task.done() for task in tasks_pages_collector]
        while not all(flag):
            print(count, queue.qsize())
            pages = await queue.get() 
            print(pages)
#            self.headers['User-Agent'] = UserAgent().random
#           async with s.get(page_href, headers=self.headers) as r:
#                if (r.status == 200):
#                    content = await r.text() 
#
#                    dom = etree.HTML(str(BeautifulSoup(content, features='lxml')))
#                    xpath = "//script[@type='application/json']"
#                    nodes_script = dom.xpath(xpath)
#                    print(len(nodes_script))
#                else:
#                    print('Failed') 
            count += 1
#            queue.task_done()
            flag = [task.done() for task in tasks_pages_collector]

    async def extract(self, 
                      hrefs: list[str]) -> dict[str, asyncio.Queue]:
        queues = {'succeeded': asyncio.Queue(), 'retry': asyncio.Queue()}
        async with aiohttp.ClientSession(headers={'Referer': ZILLOW}) as s:
            tasks_pages_collector = [asyncio.create_task(self.pages_collector(s, href, queues)) for href in hrefs]
            task = asyncio.create_task(self.homes_collector(s, queues['succeeded'], tasks_pages_collector))

            await asyncio.gather(*tasks_pages_collector, task)

            print('OK')
#            await queues['succeeded'].join()
#            for queue in queues.values():
#                await queue.join()

            # print out results
            print(f"Succeeded: {queues['succeeded'].qsize()}\nFailed: {queues['retry'].qsize()}")
            ##
        
        return queues
    
    def main(self):
        hrefs = self.cities_collector()
        queues = asyncio.run(self.extract(hrefs))

    def retry(self):
        pass