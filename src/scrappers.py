# libs
from libs import *

# URLsCollector
class URLScrapper(TableTracker):
    def __init__(self,
                 path: str, name: str, 
                 headers: dict):
        super().__init__(path, name)
        self.headers = headers

    def extract(self):
        with requests.Session() as s:
            self.headers['User-Agent'] = UserAgent().random 
            r = s.get(ZILLOW, headers=self.headers) 
            print(r.status_code)

            return r.text

    def transform(self):
        content = self.extract() 

    def load(self):
        pass