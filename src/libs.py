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
    'Accept': ' text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/wexchange;v=b3;q=0.7',
    'Accept-Encoding': ' gzip,deflate,sdch',
    'Accept-Language': ' en-US,en;q=0.8'
}
ZILLOW = 'https://www.zillow.com/'

# usr libs
from trackers import TableTracker
from scrappers import URLScrapper