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

            detailedInfo = {}
            for node in nodes_div:
                main_feature = node.xpath("./descendant::h3")[0].text

                sub_atts = {}
                for node_ul in node.xpath("./descendant::ul"):
                    node_h6_asAtt = node_ul.xpath("./preceding-sibling::h6")

                    nodes_span = node_ul.xpath("./descendant::span")
                    seperatedTexts = [[i for i in span.itertext()] for span in nodes_span]

                    noKeyTexts = []
                    a = ['"'.join(i) if (len(i) > 1) else noKeyTexts.append(i[0]) for i in seperatedTexts] 
                    a = ['{"%s"}' % i for i in a]
                    tmp_dict = {}
                    [tmp_dict.update(eval(i)) for i in a if ':' in i]
                    
                    print(noKeyTexts)
                    if node_h6_asAtt:
                        if noKeyTexts and (not tmp_dict):
                            sub_atts[node_h6_asAtt[0].text] = noKeyTexts[0]
                        else:
                            sub_atts[node_h6_asAtt[0].text] = tmp_dict

                    else:
                        sub_atts.update(tmp_dict)

                detailedInfo[main_feature] = sub_atts 
            
            print(detailedInfo)

        else:
            print('Failed')
        
foo()
eval("{'key': 'value'}")