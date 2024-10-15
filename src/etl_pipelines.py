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
        self.url_tracker = url_tracker

    def extract(self): 
        urls = self.url_tracker.retrieve(('city', 'url'))
        for name, url in urls[:2]:
            with requests.Session() as s:
                r = s.get(url, headers=self.headers)
                if r.status_code != 200:
                    continue
                else:
                    soup = BeautifulSoup(r.content.decode("utf-8"), features="lxml")
                    dom = etree.HTML(str(soup))

                    nodes_script = dom.xpath("//script[@type='application/json']")
                    script_content = nodes_script[-1].text
                    substitutions = {r'true': 'True', r'false': False, 
                                    r'null': None}
                    for sub in substitutions:
                        script_content = re.compile(sub).sub(substitutions[sub], script_content)
                    
                    script_content: dict = eval(script_content)
                    key_to_find = 'listResults'
                    while key_to_find not in script_content:
                        new = {}
                        [new.update(value) for value in script_content.values() if isinstance(value, dict)]
                        script_content = new
                    script_content = script_content[key_to_find]

    def transform(self):
        pass
    def load(self): 
        pass