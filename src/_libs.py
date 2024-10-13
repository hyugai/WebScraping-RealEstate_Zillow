# libs
import re, os, sys, time, random

# bs4
import requests
from bs4 import BeautifulSoup
from lxml import etree

# selenium
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

# data structures / databases
import numpy as np
import pandas as pd
import csv
import sqlite3

# type hint
from typing import Iterator, Literal