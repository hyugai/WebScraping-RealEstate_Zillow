# libs
import time
import json
import random
import aiohttp
import asyncio
from lxml import etree
from bs4 import BeautifulSoup
from zillow_conf import zillow

# class GeneralHomeScraper
class GeneralScraper():
    def __init__(self) -> None:
        self.zillow = zillow

    # each city href will be assigned to a worker to extract pages hrefs
    async def extract_pages_hrefs(self,
                                  s: aiohttp.ClientSession, city_href: str, 
                                  queues: dict[str, asyncio.Queue]) -> None:
        headers = random.choice(self.zillow['headers'])
        async with s.get(city_href, headers=headers) as r:
            if (r.status == 200): 
                print('OK')
                content = await r.text()

                dom = etree.HTML(str(BeautifulSoup(content, features='lxml')))
                xpath = "//li[contains(@class, 'PaginationNumberItem')]/child::a"
                nodes_a = dom.xpath(xpath)
                
                pages_hrefs = [self.zillow['homepage']+ node.get('href') for node in nodes_a]
                for href in pages_hrefs:
                    await queues['page_href'].put(href)
            else:
                print(f'Failed (error code {r.status})')
                await queues['failed_city_href'].put(city_href) 

    # each page href will wait to be assigned to 1 of N below workers to extract general homes info
    async def extract_homesFromPageHref(self, 
                                        s: aiohttp.ClientSession, queues: dict[str, asyncio.Queue]) -> None:
        while True:
            page_href = await queues['page_href'].get() 

            headers = random.choice(self.zillow['headers'])
            async with s.get(page_href, headers=headers) as r:
                if r.status == 200:
                    print('OK')

                    content = await r.text()
                    dom = etree.HTML(str(BeautifulSoup(content, features='lxml')))

                    xpath = "//script[@type='application/json' and @id='__NEXT_DATA__']"
                    nodes_script = dom.xpath(xpath)[0]

                    unfilteredJSON: dict = json.loads(nodes_script.text)
                    key_to_find = 'listResults'
                    while key_to_find not in unfilteredJSON:
                        tmp_dict = {}
                        [tmp_dict.update(value) for value in unfilteredJSON.values() if isinstance(value, dict)]
                        unfilteredJSON = tmp_dict
                    homes_asListOfDicts: list[dict] = unfilteredJSON[key_to_find]

                    keys_to_keep = ['id', 'hdpData', 'detailUrl']
                    filtered_homesInfo: list[dict] = [{key:value for key, value in home.items() if key in keys_to_keep} for home in homes_asListOfDicts]

                    await queues['home'].put(filtered_homesInfo)
                else:
                    print(f'Failed (error code{r.status})')
                    await queues['failed_page_href'].put(page_href)

            queues['page_href'].task_done()

    async def transship(self, 
                        queue: asyncio.Queue, result: list,
                        is_homes: bool=True) -> None:
        while True:
            item = await queue.get() 

            if is_homes:
                result.extend([(home['id'], json.dumps(home)) for home in item])
            else:
                result.append(item)

            queue.task_done()

    async def collect_through_city_href(self, 
                      cities_hrefs: list[str], num_workers: int=5) -> dict[str, list]: 
        queues = {'page_href': asyncio.Queue(), 'failed_city_href': asyncio.Queue(), 
                  'failed_page_href': asyncio.Queue(), 'home': asyncio.Queue()} 
        results = {'home': [], 'failed_city_href': [], 
                   'failed_page_href': []}
        async with aiohttp.ClientSession() as s:
            tasks_extract_pages_hrefs= [asyncio.create_task(self.extract_pages_hrefs(s, href, queues)) for href in cities_hrefs]
            tasks_extract_homes = [asyncio.create_task(self.extract_homesFromPageHref(s, queues)) for _ in range(num_workers)]
            tasks_transship = [asyncio.create_task(self.transship(queues['home'], results['home'])), 
                               asyncio.create_task(self.transship(queues['failed_city_href'], results['failed_city_href'], is_homes=False)), 
                               asyncio.create_task(self.transship(queues['failed_page_href'], results['failed_page_href'], is_homes=False))]

            await asyncio.gather(*tasks_extract_pages_hrefs)

            for queue in queues.values():
                await queue.join()
            
            for task in tasks_extract_homes:
                task.cancel()

            for task in tasks_transship:
                task.cancel()

        return results 
            
    def main(self, 
             cities_hrefs: list[str], num_workers: int=5) -> dict[str, list]:
        start = time.time()
        results = asyncio.run(self.collect_through_city_href(cities_hrefs, num_workers))
        print(f'Finished in: {time.time() - start}s')

        return results
