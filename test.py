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
        tets_url = 'https://www.zillow.com/homedetails/1220-Garcia-St-NE-Albuquerque-NM-87112/6772539_zpid/'
        r = s.get(tets_url, headers={'User-Agent': UserAgent().random})
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, features='lxml')
            dom = etree.HTML(str(soup))

            xpath = "//h2[text()='Facts & features']/following-sibling::div/descendant::div[@data-testid='category-group']"
            nodes_div: list[etree._Element] = dom.xpath(xpath)

            for node in nodes_div:
                feature = node.xpath("./descendant::h3")[0].text

                for node_ul in node.xpath("./descendant::ul"):
                    node_h6 = node_ul.xpath("./preceding-sibling::h6")

                    if node_h6:
                        pass 
        else:
            print('Failed')
        
foo()