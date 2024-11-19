import sys
from pathlib import Path

path_to_src = (Path.cwd()/'src').as_posix()
if path_to_src not in sys.path:
    sys.path.append(path_to_src) 
from libs import * 

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
                parentAtt= node.xpath("./descendant::h3")[0].text

                childAtts = {}
                for node_ul in node.xpath("./descendant::ul"):
                    childAtt_Name = node_ul.xpath("./preceding-sibling::h6")

                    nodes_span = node_ul.xpath("./descendant::span")
                    childAtt_Content= [[i for i in span.itertext()] for span in nodes_span]

                    noKeyTexts = [childAtt_Content.pop(i)[0] for i, val in enumerate(childAtt_Content) if (len(val) == 1)]

                    flattened_childAtt_Content = ['{"' + '"'.join(i) + '"}' for i in childAtt_Content] 
                    print(noKeyTexts, flattened_childAtt_Content)
        else:
            print('Failed')
        
foo()