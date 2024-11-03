# libs
from libs import *

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
    def __init__(self) -> None:
        pass

# https://proxyscrape.com/free-proxy-list
class ProxyScrapeScraper():
    def __init__(self) -> None:
        pass