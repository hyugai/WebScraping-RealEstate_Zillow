# bs4 
import requests
from bs4 import BeautifulSoup
from lxml import etree
from fake_useragent import UserAgent

# asynchronous
import aiohttp
import asyncio

# others
import re, sqlite3

# zillow's configs
ZILLOW_HEADERS = {
    'Accept': 'mage/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8', 
    'Accept-Encoding': 'gzip,deflate,br,zstd', 
    'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8,nl;q=0.7',
}
ZILLOW = 'https://www.zillow.com/'

# usr libs
from trackers import TableTracker
from scrappers import URLScrapper