# libs
from _libs import *
from _usr_libs import *

# class zillow city url scrapper
class CityURLScrapper():
    def __init__(self, 
                 zillow: ZillowHeadlessBrowser, table_tracker: TableTracker):
        self.zillow = zillow
        self.table_tracker = table_tracker

    def extract(self):
        self.zillow.start()
        self.zillow.find_element("//button[text()='Real Estate']").click()

    def transform(self):
        pass
    def load(self):
        pass