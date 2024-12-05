import asyncio
import pycurl
import certifi
from io import BytesIO
from curl_cffi.requests import AsyncSession
import curl_cffi
import pyppeteer
import requests
from fake_useragent import UserAgent
zillow_homepage = 'https://www.zillow.com/'
zillow_headers = {
        'Accept': '*/*', 
        'Accept-Encoding': 'gzip, deflate, br, zstd', 
        'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8,nl;q=0.7'
        }
homeDetail_href = 'https://www.zillow.com/homedetails/1531-Centra-Villa-Dr-SW-Atlanta-GA-30311/35853656_zpid/'

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

# use delay or proxies ?
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

foo5()
