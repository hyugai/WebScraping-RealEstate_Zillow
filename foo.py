import pycurl
import certifi
from io import BytesIO
from curl_cffi.requests import AsyncSession
import curl_cffi
import pyppeteer
import requests
from fake_useragent import UserAgent
from lxml import etree
from bs4 import BeautifulSoup

zillow_homepage = 'https://www.zillow.com/'
zillow_headers = {
        'Accept': '*/*', 
        'Accept-Encoding': 'gzip, deflate, br, zstd', 
        'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8,nl;q=0.7'
        }
homeDetail_href = 'https://www.zillow.com/homedetails/215-Piedmont-Ave-NE-APT-907-Atlanta-GA-30308/35881658_zpid/'

# exp
def foo1():
    with requests.Session() as s: 
        zillow_headers['User-Agent'] = UserAgent().random
        r = s.get(zillow_homepage, headers=zillow_headers)
        print(r.status_code)

# exp
async def foo2():
    browser = await pyppeteer.launch({'headless': False})
    page = await browser.newPage()
    await page.setUserAgent(UserAgent().random)
    await page.setExtraHTTPHeaders(zillow_headers)
    await page.goto(zillow_homepage)

    await page.close()

# exp
def foo3():
    c = pycurl.Curl()

    c.setopt(c.URL, homeDetail_href)

    buffer = BytesIO()
    c.setopt(c.WRITEDATA, buffer)

    c.setopt(c.CAINFO, certifi.where())

    c.perform()
    print(c.getinfo(c.RESPONSE_CODE))
    c.close()

# exp
async def foo4():
    async with AsyncSession() as s:
        r = await s.get(homeDetail_href)
        print(r.status_code)

def foo5():
    r = curl_cffi.requests.get(homeDetail_href, impersonate="safari_ios")
    print(r.status_code)

def foo6():
    with requests.Session() as s:
        r = s.get(homeDetail_href, headers={'User-Agent': UserAgent().random})
        if r.status_code == 200:
            dom = etree.HTML(str(BeautifulSoup(r.text, features="lxml")))

            xpath = "//h2[text()='Facts & features']/following-sibling::div/descendant::div[@data-testid='category-group']"
            nodes_div = dom.xpath(xpath)

            allCompounds= {} # We will have 6 "parent compounds" (~ 6 nodes) including: "Interior", "Property", "Construction", "Utilities & green energy", "Community & HOA", "Financial & listing details"

            for node in nodes_div:
                parentCompound_Name: str = node.xpath("./descendant::h3")[0].text # PARENT COMPOUND'S NAME

                parentCompound_Content= {} # PARENT COMPOUND'S CONTENT (iterate "ul"s to collect "free-text" and "sub-combound")
                for node_ul in node.xpath("./descendant::ul"): # Each "ul" node is either a "sub-combound" or "free texts" (sub-combound without the title)
                    subCompound_Name: list[etree._Element] = node_ul.xpath("./preceding-sibling::h6") # If this is empty, this "ul" node will be "free texts"
                    
                    nodes_span: list[etree._Element] = node_ul.xpath("./descendant::span") # Each node "span" consits of either 3 seprated strings or 1 single string (noted as noKeyTexts)
                    unflattened_subCompound_Content: list[list[str]]= [[i.strip() for i in span.itertext()] for span in nodes_span]

                    # Make it compatible with the others
                    noKeyTexts = ['{"Description": "%s"}' % unflattened_subCompound_Content.pop(i)[0] for i, val in enumerate(unflattened_subCompound_Content) if (len(val) == 1)]

                    flattened_subCompound_Content: list[str] = ['{"' + '"'.join(i) + '"}' for i in unflattened_subCompound_Content if (':' in i)] # len(i) != 2 -> remove "View virtual tour" / prevent error of missing ":" in key:value
                    flattened_subCompound_Content.extend(noKeyTexts) # Add fixed noKeyTexts 

                    subCompound_Content = dict()
                    [subCompound_Content.update(eval(i)) for i in flattened_subCompound_Content]

                    if subCompound_Name: 
                        parentCompound_Content[subCompound_Name[0].text] = subCompound_Content # Collect sub-compound for PARENT COMPOUND
                    else:
                        parentCompound_Content.update(subCompound_Content) # Collect free-text for PARENT COMPOUND

                allCompounds[parentCompound_Name] = parentCompound_Content

            print(allCompounds)

        else:
            print(f'Failed (error code {r.status_code})')

foo6()
