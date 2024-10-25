# libs
from _libs import *
from _usr_libs import *

# class zillow city url scrapper
class CityURLScrapper():
    def __init__(self,
                table_tracker: TableTracker, ip_tracker: IPTracker) -> None:
        self.table_tracker = table_tracker
        self.ip_tracker = ip_tracker

    def extract(self) -> Iterator[str]:
        content = self.ip_tracker.send_GETrequest(HOMEPAGE_URL, 5)
        soup = BeautifulSoup(content, features="lxml")
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

    def _extract_pages_as_doms(self, hrefs: list[str]) -> Iterator[etree._Element]:
        with requests.Session() as s:
            for href in hrefs:
                r = s.get(href, headers=self.headers)
                if r.status_code != 200:
                    print(r.status_code)
                    continue
                else:
                    soup = BeautifulSoup(r.content.decode("utf-8"), features="lxml")
                    dom = etree.HTML(str(soup))

                    yield dom
    
    # get homes data from each returned DOM object        
    # this will return each home's info as a dict enclosed in a list
    def _extract_homes(self, hrefs: list[str]) -> Iterator[list[dict]]:
        for dom in self._extract_pages_as_doms(hrefs):
            nodes_script = dom.xpath("//script[@type='application/json']")
            script_content = nodes_script[-1].text
            substitutions = {r'true': 'True', r'false': 'False', 
                            r'null': 'None'}
            for sub in substitutions:
                script_content = re.compile(sub).sub(substitutions[sub], script_content)
            
            # find list of home's info as a dict
            script_content: dict = eval(script_content)
            key_to_find = 'listResults'
            while key_to_find not in script_content:
                new = {}
                [new.update(value) for value in script_content.values() if isinstance(value, dict)]
                script_content = new
            home = script_content[key_to_find]

            yield home
                    
    # iterate the URL and perfrom extractons
    def extract(self) -> Iterator[list]: 
        urls = self.url_tracker.retrieve(['city', 'url'])
        with requests.Session() as s:
            for _, url in urls[1:2]:
                r = s.get(url, headers=self.headers)
                if r.status_code != 200:
                    continue
                else:
                    soup = BeautifulSoup(r.content.decode("utf-8"), features="lxml")
                    dom = etree.HTML(str(soup))

                    ancestor_nodes_ul = dom.xpath("//nav[@role='navigation']/child::ul")[0]
                    descendant_nodes_a = ancestor_nodes_ul.xpath("./descendant::a[contains(@title, 'Page')]")
                    hrefs = [HOMEPAGE_URL + node.get("href") for node in descendant_nodes_a]

                    homes = [home for home in self._extract_homes(hrefs)]

                    yield homes

    def transform(self):
        for homes in self.extract():
            print(homes)

    def load(self): 
        pass