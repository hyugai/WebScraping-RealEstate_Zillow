import sqlite3
import sys
import random
import requests
from lxml import etree
from bs4 import BeautifulSoup
from pathlib import Path

sys.path.append((Path.cwd()/'src').as_posix())
from zillow_conf import zillow

homeDetail_href = 'https://www.zillow.com/homedetails/215-Piedmont-Ave-NE-APT-907-Atlanta-GA-30308/35881658_zpid/'
error_homeDetail_href  = 'https://www.zillow.com/homedetails/1414-Tivoli-Hl-San-Antonio-TX-78260/122495465_zpid/'
single_quote_error = "https://www.zillow.com/homedetails/2617-Albion-St-Denver-CO-80207/13283871_zpid/"

# exp
def foo1():
    with requests.Session() as s: 
        r = s.get(zillow['homepage'], headers=random.choice(zillow['headers']))
        print(r.status_code)


def foo2(
        href: str) -> None:
    with requests.Session() as s:
        r = s.get(href, headers=random.choice(zillow['headers']))
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
                    unflattened_subCompound_Content: list[list[str]] = [[i.strip().replace('"', 'in').replace('\r\n', ' ').replace('\'', '') 
                                                                        for i in span.itertext()] for span in nodes_span]

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

# exp
def foo3():
    path_to_db = (Path.cwd()/'tests'/'resource'/'db'/'real_estate.db').as_posix()
    with sqlite3.connect(path_to_db) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM home")
        rows = cur.fetchall()
        print(rows[0])

foo3()
