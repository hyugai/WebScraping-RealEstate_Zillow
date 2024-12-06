# libs
import random 
import requests
from lxml import etree
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from zillow_conf import zillow


# function: extract cities' hrefs
def extract_cities_hrefs() -> list[str]:
    with requests.Session() as s:
        headers = random.choice(zillow['headers'])
        headers['User-Agent'] = UserAgent().random 
        r = s.get(zillow['homepage'], headers=headers) 

        if r.status_code == 200:
            print('OK')

            dom = etree.HTML(str(BeautifulSoup(r.text, features='lxml'))) 
            xpath = "//button[text()='Real Estate']/parent::div/following-sibling::ul/child::li/descendant::a"
            nodes_a = dom.xpath(xpath)
            cities_hrefs = [zillow['homepage']+ node.get('href') for node in nodes_a if node.get('href') != '/browse/homes/']

            return cities_hrefs
        else:
            raise Exception(f'Failed (error code: {r.status_code})')
