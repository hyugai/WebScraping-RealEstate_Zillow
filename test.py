import sqlite3
import requests
from lxml import etree
from pathlib import Path
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


#exp
def draft():
    db_path = (Path.cwd()/'tests'/'resource'/'db'/'real_estate.db').as_posix()
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute("select * from home")
        rows = cur.fetchall()

def foo():
    with requests.Session() as s:
        tets_url = 'https://www.zillow.com/homedetails/10789-Towner-Ave-NE-Albuquerque-NM-87112/54580242_zpid/'
        r = s.get(tets_url, headers={'User-Agent': UserAgent().random})
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, features='lxml')
            dom = etree.HTML(str(soup))

            xpath = "//h2[text()='Facts & features']/following-sibling::div/descendant::div[@data-testid='category-group']"
            nodes_div = dom.xpath(xpath)

            allInfo = {}
            for node in nodes_div:
                parentAtt_Name: str = node.xpath("./descendant::h3")[0].text

                childAtts = {}
                for node_ul in node.xpath("./descendant::ul"):
                    childAtt_Name: list[etree._Element] = node_ul.xpath("./preceding-sibling::h6")

                    nodes_span: list[etree._Element] = node_ul.xpath("./descendant::span")
                    childAtt_Content: list[list[str]]= [[i for i in span.itertext()] for span in nodes_span]

                    noKeyTexts = ['{"Description": "%s"}' % childAtt_Content.pop(i)[0] for i, val in enumerate(childAtt_Content) if (len(val) == 1)]

                    flattened_childAtt_Content: list[str] = ['{"' + '"'.join(i) + '"}' for i in childAtt_Content] 
                    flattened_childAtt_Content.extend(noKeyTexts)

                    tmp_dict = dict()
                    [tmp_dict.update(eval(i)) for i in flattened_childAtt_Content]

                    if childAtt_Name:
                        childAtts[childAtt_Name[0].text] = tmp_dict 
                    else:
                            childAtts.update(tmp_dict)

                allInfo[parentAtt_Name] = childAtts

            print(allInfo)
        else:
            print('Failed')
        
foo()
