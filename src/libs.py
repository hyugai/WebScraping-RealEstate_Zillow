# bs4 
import requests
from bs4 import BeautifulSoup
from lxml import etree
from fake_useragent import UserAgent

# asynchronous
import aiohttp
import asyncio

# playwright
from playwright.async_api import async_playwright, Playwright, Page

# data structure
import numpy as np
import pandas as pd

# others
import re, sqlite3
from datetime import datetime

# zillow's configs
ZILLOW_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/wexchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip,deflate,sdch', 'Accept-Language': 'en-US,en;q=0.8', 
    'Referer': 'https://www.google.com.vn'
}
ZILLOW = 'https://www.zillow.com'

# usr libs
from trackers import * 
from zillow import URLScraper, GeneralHomeScraper 
from proxies import FreeProxyListScraper, GeonodeScraper 