# libs
import time
import json
import aiohttp
import asyncio
from lxml import etree
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# zillow's config
ZILLOW_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/wexchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip,deflate,sdch', 'Accept-Language': 'en-US,en;q=0.8', 
    'Referer': 'https://www.google.com.vn'
}
ZILLOW = 'https://www.zillow.com'

# class DetailedHomesScraper
"""
We will have 6 "parent compounds" (~ 6 nodes) including: "Interior", "Property", "Construction", "Utilities & green energy", "Community & HOA", "Financial & listing details"
Each node -> 2 sub-nodes: 
     -> the 1st one contains the PARENT COMPOUND'S NAME
     -> the 2nd one is the CONTENT ("free-text" & "sub-compound") of it 
 """
class ExtendedScraper():
    def __init__(self) -> None:
        self.headers = ZILLOW_HEADERS 

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

                    allCompounds= {}

                    for node in nodes_div:
                        # PARENT COMPOUND'S NAME
                        parentCompound_Name: str = node.xpath("./descendant::h3")[0].text

                        parentCompound_Content= {}
                        # PARENT COMPOUND'S CONTENT (iterate "ul"s to collect "free-text" and "sub-combound")
                        # Each "ul" node is either a "sub-combound" or "free texts" (sub-combound without the title)
                        for node_ul in node.xpath("./descendant::ul"):
                            # If this is empty, this "ul" node will be "free texts"
                            subCompound_Name: list[etree._Element] = node_ul.xpath("./preceding-sibling::h6")

                            # Each node "span" consits of either 3 seprated strings or 1 single string (noted as noKeyTexts)
                            nodes_span: list[etree._Element] = node_ul.xpath("./descendant::span")
                            unflattened_subCompound_Content: list[list[str]]= [[i.strip() for i in span.itertext()] for span in nodes_span]

                            # Make it compatible with the others
                            noKeyTexts = ['{"Description": "%s"}' % unflattened_subCompound_Content.pop(i)[0] for i, val in enumerate(unflattened_subCompound_Content) if (len(val) == 1)]

                            flattened_subCompound_Content: list[str] = ['{"' + '"'.join(i) + '"}' for i in unflattened_subCompound_Content if len(i) != 2] # len(i) != 2 -> remove "View virtual tour"
                            # Add fixed noKeyTexts 
                            flattened_subCompound_Content.extend(noKeyTexts)

                            subCompound_Content = dict()
                            [subCompound_Content.update(eval(i)) for i in flattened_subCompound_Content]
                            print(subCompound_Content)

                            if subCompound_Name: 
                                # Collect sub-compound for PARENT COMPOUND
                                parentCompound_Content[subCompound_Name[0].text] = subCompound_Content

                            else:
                                # Collect free-text for PARENT COMPOUND
                                parentCompound_Content.update(subCompound_Content)

                        allCompounds[parentCompound_Name] = parentCompound_Content
                    
                    await queues['home'].put((home_id, allCompounds))
                else:
                    print(f'Failed (error code: {r.status})')
                    await queues['failed_href'].put(href)

            queues['href'].task_done()

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

            queue.task_done()


    async def collect(self,
                      href: asyncio.Queue, num_workers: int=5) -> dict[str, list]:
        queues = {'href': href, 'failed_href': asyncio.Queue(),
                  'home': asyncio.Queue()}
        results = {'failed_href': [], 'home': []}

        async with aiohttp.ClientSession(headers={'Referer': ZILLOW}) as s:
            tasks_extract_homeDetails = [asyncio.create_task(self.extract_detailedInfo(s, queues)) for _ in range(num_workers)]
            tasks_transship = [asyncio.create_task(self.transship(queues['home'], results['home'])), 
                               asyncio.create_task(self.transship(queues['failed_href'], results['failed_href'], is_home=False))] 
            
            asyncio.gather(*tasks_extract_homeDetails)

            for q in queues.values():
                await q.join()

            for t in tasks_extract_homeDetails:
                t.cancel()

            for t in tasks_transship:
                t.cancel()

        return results
