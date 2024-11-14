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
            nodes_div = dom.xpath(xpath)
            # test
            single_node_div = nodes_div[0]

            xpath = "./descendant::h3"
            node_h3 = single_node_div.xpath(xpath)[0]
            xpath = "./child::div[2]/child::div" 
            child_nodes_div = single_node_div.xpath(xpath)
            
            print(type(child_nodes_div[0]))
            for i in child_nodes_div[0].xpath("./descendant::span")[0].itertext():
                print(i)
            ##
#            for node in nodes_div:
#                print(node.xpath("./descendant::h3")[0].text)
        else:
            print('Failed')
        
foo()