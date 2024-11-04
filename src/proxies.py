# libs
from libs import *
import json

# https://free-proxy-list.net/
class FreeProxyListScraper():
    global HOMEPAGE
    HOMEPAGE = 'https://free-proxy-list.net/'

    def __init__(self, 
                 headers: dict[str, str], csv_path: str) -> None:
        self.headers = headers 
        self.csv_path = csv_path
    
    def extract(self) -> dict[str, list]:
        with requests.Session() as s:
            self.headers['User-Agent'] = UserAgent().random
            r = s.get(HOMEPAGE, headers=self.headers)
            if r.status_code == 200:
                content = r.content.decode('utf-8')
                dom = etree.HTML(str(BeautifulSoup(content, features='lxml')))

                xpath = "//h1[text()='Free Proxy List']/parent::div/following-sibling::div/descendant::table"
                node_table = dom.xpath(xpath)[0]

                xpath = "./descendant::th"
                nodes_th = node_table.xpath(xpath)
                columns = [node.text for node in nodes_th]
                collected_proxies = {key: [] for key in columns}
            
                xpath = "./descendant::tr"
                nodes_tr = node_table.xpath(xpath)
            
                xpath = "./child::td"
                for node in nodes_tr:
                    [collected_proxies[columns[i]].append(td.text) for i, td in enumerate(node.xpath(xpath))]

                return collected_proxies
            else:
                raise Exception(f'Failed fetching (error code: {r.status_code})')

    def transform(self):
        proxies = self.extract() 
        proxies = {key.lower().replace(' ', '_'): value for (key, value) in proxies.items()}
        proxies['scraped_date'] = [datetime.now().strftime(r'%d-%m-%Y %H:%M:%S')]*len(proxies['port'])

        return proxies

    def load(self):
        proxies = self.transform() 
        pd.DataFrame(proxies).to_csv(self.csv_path, index=False)

# https://geonode.com/free-proxy-list
class GeonodeScraper():
    global homepage, api_endpoint, params
    homepage = 'https://geonode.com/free-proxy-list'
    api_endpoint = 'https://proxylist.geonode.com/api/proxy-list'
    params = {'limit': 500, 'sort_by': 'lastChecked', 'sort_type': 'desc'}

    def __init__(self, 
                 headers: dict[str, str]) -> None:
        self.headers = headers 

    async def calculate_numberOfPages(self,
                                      p: Playwright):
        browser = await p.chromium.launch(headless=False) 
        context = await browser.new_context(user_agent=UserAgent().random)
        page = await context.new_page()
        
        await page.goto(homepage)

        xpath = "//p[text()='Proxies online']/parent::span/following-sibling::p"
        node_p = page.locator(selector=f"xpath={xpath}")
        
        numberOf_onlineProxies = await node_p.inner_text()
        quotient, _ = divmod(int(numberOf_onlineProxies.replace(',', '')), 500)
        numberOf_pages = quotient + 1

        return numberOf_pages

    async def extract_json(self, 
                           s: aiohttp.ClientSession, page: int, 
                           queue: asyncio.Queue) -> None:
        params['page'] = page 
        async with s.get(api_endpoint, params=params) as r:
            content = await r.text()
            await queue.put(json.loads(content))

    async def extract_api_urls(self):
        async with async_playwright() as p:
            task_calculate = asyncio.create_task(self.calculate_numberOfPages(p)) 
            numberOf_pages = await task_calculate
            print(numberOf_pages)
            
        queue = asyncio.Queue()
        async with aiohttp.ClientSession() as s:
            tasks_extract_proxies = [asyncio.create_task(self.extract_json(s, page, queue)) for page in range(1, numberOf_pages + 1)] 
            await asyncio.gather(*tasks_extract_proxies)

    def main(sefl):
        asyncio.run(sefl.extract_api_urls())

# https://proxyscrape.com/free-proxy-list
class ProxyScrapeScraper():
    def __init__(self) -> None:
        pass