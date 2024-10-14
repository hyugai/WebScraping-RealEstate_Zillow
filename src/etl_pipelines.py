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

    def extract(self) -> Iterator[str]:
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

                for li in child_nodes_li:
                    descendant_node_a = li.xpath("./descendant::a")[0]
                    partial_city_url = descendant_node_a.get("href")

                    yield partial_city_url

    def transform(self) -> Iterator[tuple[str, str]]:
        for partial_url in self.extract():
            name = partial_url.strip().lower().\
                replace('/', '').replace('-', '_')
            complete_url = HOMEPAGE_URL + partial_url

            yield (name, complete_url)

    def load(self) -> None:
        uniq_column, all_columns = 'city', ('city', 'url')
        self.table_tracker.create(uniq_column, all_columns)
        for record in self.transform():
            self.table_tracker.insert(all_columns, record)

class GeneralHomeScrapper_RE():
    def __init__(self, 
                 headers: dict, 
                 home_tracker: TableTracker, url_tracker: TableTracker) -> None:
        self.headers = headers
        self.home_tracker = home_tracker
        self.url_tracker - url_tracker

    