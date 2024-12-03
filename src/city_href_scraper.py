# libs
import requests
from lxml import etree
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# zillow's config
ZILLOW_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/wexchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip,deflate,sdch', 'Accept-Language': 'en-US,en;q=0.8', 
    'Referer': 'https://www.google.com.vn'
}
ZILLOW = 'https://www.zillow.com'

# function: extract cities' hrefs
def extract_cities_hrefs() -> list[str]:
    with requests.Session() as s:
        ZILLOW_HEADERS['User-Agent'] = UserAgent().random 
        r = s.get(ZILLOW, headers=ZILLOW_HEADERS) 

        if r.status_code == 200:
            print('OK')

            dom = etree.HTML(str(BeautifulSoup(r.text, features='lxml'))) 
            xpath = "//button[text()='Real Estate']/parent::div/following-sibling::ul/child::li/descendant::a"
            nodes_a = dom.xpath(xpath)
            cities_hrefs = [ZILLOW + node.get('href') for node in nodes_a if node.get('href') != '/browse/homes/']

            return cities_hrefs
        else:
            raise Exception(f'Failed (error code: {r.status_code})')
