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

            # test 01
            detailInfo_asDict = dict()
            for node in nodes_div:
                child_nodes_div: list[etree._Element] = node.xpath("./child::div")

                descendant_node_h3_asMainKey = child_nodes_div[0].xpath("./descendant::h3")[0].text
                detailInfo_asDict[descendant_node_h3_asMainKey] = None

                descendant_nodes_div_asSubElements: list[etree._Element] = child_nodes_div[1].xpath("./child::div")
                for ele in descendant_nodes_div_asSubElements:
                    try:
                        node_h6_asSubkey = ele.xpath("./child::h6")[0].text
                    except:
                        print(node_h6_asSubkey)
                    nodes_span: list[etree._Element] = ele.xpath("./descendant::span")

                    a = [''.join(span.itertext()) for span in nodes_span]
                    print(a)
            ##

            # test
#            single_node_div = nodes_div[0]
#
#            xpath = "./descendant::h3"
#            node_h3 = single_node_div.xpath(xpath)[0]
#            xpath = "./child::div[2]/child::div" 
#            child_nodes_div: list[etree._Element] = single_node_div.xpath(xpath)
#            
#            for i in child_nodes_div[1].xpath("./descendant::span")[0].itertext():
#                print(i)
            ##
        else:
            print('Failed')
        
foo()