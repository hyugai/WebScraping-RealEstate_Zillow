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

            main = {}
            for node in nodes_div:
                feature = node.xpath("./descendant::h3")[0].text

                subs = {}
                for node_ul in node.xpath("./descendant::ul"):
                    node_h6 = node_ul.xpath("./preceding-sibling::h6")

                    nodes_span = node_ul.xpath("./descendant::span")
                    x = [[i for i in span.itertext()] for span in nodes_span]
                    b = []
                    a = ['"'.join(i) if (len(i) > 1) else b.append(i[0]) for i in x] 
                    a = ['{"%s"}' % i for i in a]
                    tmp_dict = {}
                    [tmp_dict.update(eval(i)) for i in a if ':' in i]
                    
                    if node_h6:
                        if b and (not tmp_dict):
                            subs[node_h6[0].text] = b[0]
                        else:
                            subs[node_h6[0].text] = tmp_dict

                    else:
                        subs.update(tmp_dict)

                main[feature] = subs
            
            print(main)

        else:
            print('Failed')
        
foo()
eval("{'key': 'value'}")