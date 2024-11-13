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

with requests.Session() as s:
    tets_url = 'https://www.zillow.com/homedetails/1220-Garcia-St-NE-Albuquerque-NM-87112/6772539_zpid/'
    r = s.get(tets_url, headers={'User-Agent': UserAgent().random})
    if r.status_code == 200:
        print('OK')
        dom = etree.HTML(str(BeautifulSoup(r.text, features='lxml')))

        xpath = "//h2[text()='Facts & features']"
        node_h2 = dom.xpath(xpath)[0]
        print(node_h2.text)
    else:
        print('Failed')