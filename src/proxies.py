# libs
from libs import *

# https://free-proxy-list.net/
class FreeProxyListScraper():
    global HOMEPAGE
    HOMEPAGE = 'https://free-proxy-list.net/'

    def __init__(self, 
                 headers: dict[str, str]) -> None:
        self.headers = headers 
    
    def extract(self):
        with requests.Session() as s:
            self.headers['User-Agent'] = UserAgent().random
            r = s.get(HOMEPAGE, headers=self.headers)
            if r.status_code == 200:
                content = r.content.decode('utf-8')

                dom = etree.HTML(str(BeautifulSoup(content, features='lxml')))
                xpath = "//h1[text()='Free Proxy List']/parent::div/following-sibling::div/descendant::table"
                node_table = dom.xpath(xpath)
                print(node_table)
            else:
                raise Exception(f'Failed fetching (error code: {r.status_code})')

    def transform(self):
        pass

    def load(self):
        pass

# https://geonode.com/free-proxy-list
class GeonodeScraper():
    def __init__(self) -> None:
        pass

# https://proxyscrape.com/free-proxy-list
class ProxyScrapeScraper():
    def __init__(self) -> None:
        pass