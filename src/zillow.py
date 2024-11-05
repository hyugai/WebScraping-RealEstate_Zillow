# libs
import aiohttp.client_exceptions
from libs import *
from aiohttp_socks import ProxyConnector

# URLsCollector
class URLScraper():
    def __init__(self,
                 headers: dict[str, str], proxies_pool: list) -> None:
        self.headers = headers
        self.proxies_pool = proxies_pool

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
                raise Exception(f'Failed fetching (error code: {r.status_code})')

    async def extract_pages_hrefs(self,
                                s: aiohttp.ClientSession, city_href: str, 
                                queues: dict[str, asyncio.Queue]) -> None:
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

    async def transship(self,
                        collected_hrefs: list, queue: asyncio.Queue):
        while True:
            href = await queue.get()
            collected_hrefs.append(href)

            queue.task_done()
    
    async def collect(self, 
                      hrefs: list[str]) -> dict[str, list]:
        all_hrefs = {'succeeded': [], 'retry': []}
        queues = {'succeeded': asyncio.Queue(), 'retry': asyncio.Queue()}
        async with aiohttp.ClientSession(headers={'Referer': ZILLOW}) as s:
            tasks_pages_collector = [asyncio.create_task(self.extract_pages_hrefs(s, href, queues)) for href in hrefs]
            tasks_transship = [asyncio.create_task(self.transship(a, b)) for a, b in zip(all_hrefs.values(), queues.values())] 

            await asyncio.gather(*tasks_pages_collector)
            
            for queue in queues.values():
                await queue.join()
            for task in tasks_transship:
                task.cancel() 

            # print out results
            for key, value in all_hrefs.items():
                print(f'{key}: {len(value)}') 
            ##
        
        return all_hrefs 
    
    def main(self):
        cities_hrefs = self.extract_cities_hrefs()
        all_hrefs = asyncio.run(self.collect(cities_hrefs))

        return all_hrefs 

    def retry(self):
        pass


class GeneralHomeScraper():
    def __init__(self, 
                 headers: dict[str, str], pages_hrefs: list[str]) -> None:
        self.headers = headers
        self.pages_hrefs = pages_hrefs

    async def transship(self) -> None:
        pass

    async def homes_extractor(self, 
                              s: aiohttp.ClientSession, href: str, 
                              queues: dict[str, asyncio.Queue]) -> None:
        self.headers['User-Agent'] = UserAgent().random
        try:
            async with s.get(href, headers=self.headers) as r:
                if (r.status == 200):
                    print('OK')
                    content = await r.text() 
                    await queues['succeeded'].put(content)

    #                dom = etree.HTML(str(BeautifulSoup(content, features='lxml')))
    #                xpath = "//script[@type='application/json']"
    #                nodes_script = dom.xpath(xpath)
    #                print(len(nodes_script))
                else:
                    content = await r.text()
                    await queues['retry'].put(href) 
        except (aiohttp.ConnectionTimeoutError, aiohttp.ClientOSError):
            print('Failed')

    async def collect(self) -> None:
        async with aiohttp.ClientSession(headers={'Referer': ZILLOW}) as s:
            queues = {'succeeded': asyncio.Queue(), 'retry': asyncio.Queue()}
            tasks_homes_extractor = [asyncio.create_task(self.homes_extractor(s, href, queues)) for href in self.pages_hrefs] 

            await asyncio.gather(*tasks_homes_extractor)

            # print results
            for name, queue in queues.items():
                print(f'{name}: {queue.qsize()}')
            ##

    def main(self):
        asyncio.run(self.collect()) 