# libs
from pandas.core.construction import range_to_ndarray
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from lxml import etree
import aiohttp
import asyncio
import json
import time
ZILLOW_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/wexchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip,deflate,sdch', 'Accept-Language': 'en-US,en;q=0.8', 
    'Referer': 'https://www.google.com.vn'
}
ZILLOW = 'https://www.zillow.com'

# function: extract cities' hrefs
def extract_cities_hrefs(
                         headers: dict[str, str]) -> list[str]:
    with requests.Session() as s:
        headers['User-Agent'] = UserAgent().random 
        r = s.get(ZILLOW, headers=headers) 

        if r.status_code == 200:
            print('OK')

            dom = etree.HTML(str(BeautifulSoup(r.text, features='lxml'))) 
            xpath = "//button[text()='Real Estate']/parent::div/following-sibling::ul/child::li/descendant::a"
            nodes_a = dom.xpath(xpath)
            cities_hrefs = [ZILLOW + node.get('href') for node in nodes_a if node.get('href') != '/browse/homes/']

            return cities_hrefs
        else:
            raise Exception(f'Failed (error code: {r.status_code})')

# class GeneralHomeScraper
class GeneralHomesScraper():
    def __init__(self,
                 headers: dict[str, str]) -> None:
        self.headers = headers

    # each city href will be assigned to a worker to extract pages hrefs
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
                    await queues['page_href'].put(href)
            else:
                await queues['failed_city_href'].put(city_href) 

    # each page href will wait to be assigned to 1 of N below workers to extract general homes info
    async def extract_homesFromPageHref(self, 
                                        s: aiohttp.ClientSession, queues: dict[str, asyncio.Queue]) -> None:
        while True:
            page_href = await queues['page_href'].get() 

            self.headers['User-Agent'] = UserAgent().random
            async with s.get(page_href, headers=self.headers) as r:
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
                    print(f'Failed to extract homes: {r.status}')
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

    async def collect(self, 
                      cities_hrefs: list[str], num_homes_extractors: int=5) -> dict[str, list]: 
        queues = {'page_href': asyncio.Queue(), 'failed_city_href': asyncio.Queue(), 
                  'failed_page_href': asyncio.Queue(), 'home': asyncio.Queue()} 
        results = {'home': [], 'failed_city_href': [], 
                   'failed_page_href': []}
        async with aiohttp.ClientSession(headers={'Referer': ZILLOW}) as s:
            tasks_extract_pages_hrefs= [asyncio.create_task(self.extract_pages_hrefs(s, href, queues)) for href in cities_hrefs]
            tasks_extract_homes = [asyncio.create_task(self.extract_homesFromPageHref(s, queues)) for _ in range(num_homes_extractors)]
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
            # results
            ##

        return results 
            
    def main(self, 
             cities_hrefs: list[str]) -> dict[str, list]:
        start = time.time()
        results = asyncio.run(self.collect(cities_hrefs))
        print(f'Finished in: {time.time() - start}')

        return results

# class DetailedHomesScraper
class DetailedHomesScraper():
    def __init__(self, 
                 headers: dict[str, str]) -> None:
        self.headers = headers 

    async def extract_detailedInfo(self, 
                                   s: aiohttp.ClientSession, queues: dict[str, asyncio.Queue]) -> None:
        while True:
            home_id, href = await queues['href'].get()
            self.headers['User-Agent'] = UserAgent().random
            async with s.get(href, headers=self.headers) as r:
                if r.status == 200:
                    print('OK')

                    content = await r.text()
                    dom = etree.HTML(str(BeautifulSoup(content, features='lxml')))

                    xpath = "//h2[text()='Facts & features']/following-sibling::div/descendant::div[@data-testid='category-group']"
                    nodes_div = dom.xpath(xpath)

                    # allInfo will have 6 "parent compounds" (~ 6 nodes) including: "Interior", "Property", "Construction", "Utilities & green energy", "Community & HOA", "Financial & listing details"
                    allCompounds= {}

                    # Each node -> 2 sub-nodes: 
                    # -> the 1st one contains the PARENT COMPOUND'S NAME
                    # -> the 2nd one is the CONTENT ("free-text" & "sub-compound") of it 
                    for node in nodes_div:
                        # PARENT COMPOUND'S NAME
                        parentCompound_Name: str = node.xpath("./descendant::h3")[0].text

                        parentCompound_Content= {}
                        # PARENT COMPOUND'S CONTENT (iterate "ul"s to collect "free-text" and "sub-combound")
                        for node_ul in node.xpath("./descendant::ul"):
                            # each "ul" node is either a "sub-combound" or "free texts" (sub-combound without the title)
                            # if this is empty, this "ul" node will be "free texts"
                            subCompound_Name: list[etree._Element] = node_ul.xpath("./preceding-sibling::h6")

                            # each node "span" consits of either 3 seprated strings or 1 single string (noted as noKeyTexts)
                            nodes_span: list[etree._Element] = node_ul.xpath("./descendant::span")
                            unflattened_subCompound_Content: list[list[str]]= [[i for i in span.itertext()] for span in nodes_span]

                            # make it compatible with the others
                            noKeyTexts = ['{"Description": "%s"}' % unflattened_subCompound_Content.pop(i)[0] for i, val in enumerate(unflattened_subCompound_Content) if (len(val) == 1)]

                            flattened_subCompound_Content: list[str] = ['{"' + '"'.join(i) + '"}' for i in unflattened_subCompound_Content] 
                            # add fixed noKeyTexts 
                            flattened_subCompound_Content.extend(noKeyTexts)

                            subCompound_Content = dict()
                            [subCompound_Content.update(eval(i)) for i in flattened_subCompound_Content]

                            if subCompound_Name:
                                # collect sub-compound for PARENT COMPOUND
                                parentCompound_Content[subCompound_Name[0].text] = subCompound_Content
                            else:
                                # collect free-text for PARENT COMPOUND
                                parentCompound_Content.update(subCompound_Content)

                        allCompounds[parentCompound_Name] = parentCompound_Content
                    
                    await queues['home'].put((home_id, allCompounds))
                else:
                    print(f'Failed (error code: {r.status})')
                    await queues['failed_href'].put(href)

    async def transship(self,
                        queue: asyncio.Queue, results: list, 
                        is_home: bool=True) -> None:
        while True:
            item: tuple[int, dict] | str = await queue.get() 
            if is_home:
                home_id, homeDetails = item
                results.append((home_id, json.dumps(homeDetails)))
            else:
                results.append(item)


    async def collect(self,
                      href: asyncio.Queue, num_homeDetails_extractor: int=5) -> None:
        queues = {'href': href, 'failed_href': asyncio.Queue(),
                  'home': asyncio.Queue()}
        results = {'failed_href': [], 'home': []}

        async with aiohttp.ClientSession(headers={'Referer': ZILLOW}) as s:
            tasks_extract_homeDetails = [asyncio.create_task(self.extract_detailedInfo(s, queues)) for _ in range(num_homeDetails_extractor)]
            tasks_transship = [asyncio.create_task(self.transship(queues['home'], results['home'])), 
                               asyncio.create_task(self.transship(queues['failed_href'], results['failed_href'], is_home=False))] 

            asyncio.gather(*tasks_extract_homeDetails)

            [t.cancel() for t in tasks_transship]
            [await q.join() for q in queues.values()]
            
    def main(self, 
             href: asyncio.Queue, num_homeDetails_extractor: int=5):
        asyncio.run(self.collect(href, num_homeDetails_extractor)) 
