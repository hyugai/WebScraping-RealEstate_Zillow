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

    async def push_into_queue(self, 
                              item, queue: asyncio.Queue) -> None:
        await queue.put(item)

    # each city href will be assigned to a worker to extract pages hrefs
    async def extractPagesHrefs(self,
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
                print(f'Failed (error code: {r.status})')
                await queues['failed_city_href'].put([city_href]) 

    # each page href will wait to be assigned to 1 of N below workers to extract general homes info
    """
    queues['page_href'] is the default source to get the pages' hrefs
    queues['home'] is the default source to store successful scraping
    queues['failed_page_href'] is the default source to store pages' hrefs failed to scrape
    """
    async def extractHomes_fromPageHref(self, 
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
                    key_toFind = 'listResults'
                    while key_toFind not in unfilteredJSON:
                        tmp_dict = {}
                        [tmp_dict.update(value) for value in unfilteredJSON.values() if isinstance(value, dict)]
                        unfilteredJSON = tmp_dict

                    homes_toPushIntoDB: list[tuple[int, str, str]] = [(info.pop('id'), json.dumps(info.pop('hdpData')), info.pop('detailUrl')) # convert to suitable format to push into the database
                                          for info in unfilteredJSON[key_toFind]] 

                    await queues['home'].put(homes_toPushIntoDB) 
                else:
                    print(f'Failed (error code: {r.status})')
                    await queues['failed_page_href'].put(page_href) 

            queues['page_href'].task_done()

    async def transship(self, 
                        queue: asyncio.Queue, result: list) -> None:
        while True:
            item = await queue.get() 
            result.extend(item)

            queue.task_done()

    async def collectHomes_throughCityHref(self, 
                      cities_hrefs: list[str], num_workers: int=5) -> dict[str, list]: 
        queues = {'page_href': asyncio.Queue(), 'failed_city_href': asyncio.Queue(), 
                  'failed_page_href': asyncio.Queue(), 'home': asyncio.Queue()} 
        results = {'home': [], 'failed_city_href': [], 
                   'failed_page_href': []}
        async with aiohttp.ClientSession() as s:
            tasks_extract_pages_hrefs= [asyncio.create_task(self.extractPagesHrefs(s, href, queues)) for href in cities_hrefs]
            tasks_extract_homes = [asyncio.create_task(self.extractHomes_fromPageHref(s, queues)) for _ in range(num_workers)]
            tasks_transship = [asyncio.create_task(self.transship(queues['home'], results['home'])), 
                               asyncio.create_task(self.transship(queues['failed_city_href'], results['failed_city_href'])), 
                               asyncio.create_task(self.transship(queues['failed_page_href'], results['failed_page_href']))]

            await asyncio.gather(*tasks_extract_pages_hrefs)

            [await q.join() for q in queues.values()]
            [t.cancel() for t in  tasks_extract_homes]
            [t.cancel() for t in tasks_transship]

        return results 

    async def collectHomes_throughPageHref(self, 
                                        pages_hrefs: list[str], num_workers: int=5):
        queues = {'page_href': asyncio.Queue(), 'failed_page_href': asyncio.Queue(), 
                  'home': asyncio.Queue()}
        results = {'home': [], 'failed_page_href': []}

        async with aiohttp.ClientSession() as s:
            tasks_push_hrefs = [asyncio.create_task(self.push_into_queue(href, queues['page_href'])) 
                                    for href in pages_hrefs]
            tasks_extract_homes = [asyncio.create_task(self.extractHomes_fromPageHref(s, queues)) for _ in range(num_workers)]
            tasks_transship = [asyncio.create_task(self.transship(queues['home'], results['home'])), 
                               asyncio.create_task(self.transship(queues['failed_page_href'], results['failed_page_href']))]

            asyncio.gather(*tasks_push_hrefs)

            [await q.join() for q in queues.values()]
            [t.cancel() for t in tasks_extract_homes]
            [t.cancel() for t in tasks_transship]

        return results
            
    def main(self, 
             cities_hrefs: list[str], num_workers: int=5) -> dict[str, list]:
        start = time.time()
        results = asyncio.run(self.collectHomes_throughCityHref(cities_hrefs, num_workers))
        print(f'Finished in: {time.time() - start}s')

        return results
