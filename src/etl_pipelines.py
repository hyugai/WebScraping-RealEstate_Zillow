# libs
from _libs import *
from _usr_libs import *

# class zillow city url scrapper
class CityURLScrapper():
    def __init__(self,
                 headers: dict,
                table_tracker: TableTracker) -> None:
        self.headers = headers
        self.table_tracker = table_tracker

    def extract(self):
        with requests.Session() as s:
            r = s.get(HOMEPAGE_URL, headers=self.headers)
            if r.status_code != 200:
                print(r.status_code)
            else:
                soup = BeautifulSoup(r.content.decode("utf-8"), features="lxml")
                dom = etree.HTML(str(soup))

                node_div = dom.xpath("//button[text()='Real Estate']/parent::div")[0]
                sibling_node_ul = node_div.xpath("./following-sibling::ul")[0]
                child_nodes_li = sibling_node_ul.xpath("./child::li")

                print(len(child_nodes_li))
    def transform(self):
        pass
    def load(self):
        pass