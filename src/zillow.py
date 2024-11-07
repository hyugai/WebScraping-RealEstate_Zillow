# libs
import aiohttp.client_exceptions
from libs import *

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
                 headers: dict[str, str], proxies_pool: list[str]) -> None:
        self.headers = headers
        self.proxies_pool = proxies_pool

    async def transship_collectedHomes(self,
                                       collectedHomes: list, queue: asyncio.Queue) -> None:
        while True:
            homes_asJSON = await queue.get() 
            collectedHomes.extend([(home['id'], json.dumps(home)) for home in homes_asJSON])

            queue.task_done()

    async def transship_hrefsToRetry(self,
                                     hrefsToRetry: list, queue: asyncio.Queue) -> None:
        while True:
            href = await queue.get() 
            hrefsToRetry.append(href)
            
            queue.task_done()

    async def homes_extractor(self, 
                              s: aiohttp.ClientSession, href: str, 
                              queues: dict[str, asyncio.Queue], numberOf_trials: int=3) -> None:
        trial = 1
        while trial <= numberOf_trials:
            self.headers['User-Agent'] = UserAgent().random
            try:
                async with s.get(href, headers=self.headers, proxy=random.choice(self.proxies_pool)) as r:
                    if (r.status == 200):
                        print(f'Trial {trial}: OK')
                        content = await r.text() 
                        dom = etree.HTML(str(BeautifulSoup(content, features='lxml')))

                        xpath = "//script[@type='application/json']"
                        nodes_script = dom.xpath(xpath)

                        unfilteredJSON: dict = json.loads(nodes_script[2].text)
                        key_to_find = 'listResults'
                        while key_to_find not in unfilteredJSON:
                            tmp_dict = {}
                            [tmp_dict.update(value) for value in unfilteredJSON.values() if isinstance(value, dict)]
                        homes_asJSON: list[dict] = unfilteredJSON[key_to_find]

                        await queues['succeeded'].put(homes_asJSON)
                        
                        break
                    else:
                        print(f'Trial {trial}: Failed fetching (error code: {r.status})')
            except Exception as e:
                print(f'Trial {trial}: {e}') 
            finally:
                if trial == numberOf_trials:
                    await queues['retry'].put(href)
                trial += 1

    async def collect(self, 
                      pages_hrefs: list[str]) -> tuple[list, list]:
        queues = {'succeeded': asyncio.Queue(), 'retry': asyncio.Queue()}
        collectedHomes, hrefsToRetry = [], []

        async with aiohttp.ClientSession(headers={'Referer': 'https://www.google.com.vn'}) as s:
            tasks_homes_extractor = [asyncio.create_task(self.homes_extractor(s, href, queues)) for href in pages_hrefs] 
            tasks_transship = [asyncio.create_task(self.transship_collectedHomes(collectedHomes, queues['succeeded'])), 
                               asyncio.create_task(self.transship_hrefsToRetry(hrefsToRetry, queues['retry']))]

            await asyncio.gather(*tasks_homes_extractor)
            
            for queue in queues.values():
                await queue.join()
            for task in tasks_transship:
                task.cancel()

        return collectedHomes, hrefsToRetry

    def main(self, 
             pages_hrefs: list[str]) -> tuple[list, list]:
        start = time.time() 
        collectedHomes, hrefsToRetry = asyncio.run(self.collect(pages_hrefs))
        print(f'Finished in: {time.time() - start}s')

        return collectedHomes, hrefsToRetry