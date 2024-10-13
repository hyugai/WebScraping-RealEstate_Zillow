# libs
import os, sys
cwd = os.getcwd()
os.chdir('src/'); path_to_src = os.getcwd()
os.chdir(cwd)
if path_to_src not in sys.path:
    sys.path.append(path_to_src)

from _libs import *
from _usr_libs import *

# exp
test_url = "https://www.zillow.com/"
headers = {'User-Agent': random.choice(USER_AGENTS),
           'Accept-Language': ACCEPT_LANGUAGE, 'Accept-Encoding': ACCEPT_ENCODING}

with requests.Session() as s:
    r = s.get(test_url, headers=headers)
    if r.status_code != 200:
        print(r.status_code)
    else:
        soup = BeautifulSoup(r.content.decode("utf-8"), features="lxml")
        dom = etree.HTML(str(soup))

        sibling_node_div = dom.xpath("//button[text()='Real Estate']/parent::div")[0]
        sibling_nodes_ul = sibling_node_div.xpath("./following-sibling::ul")[0]
        child_nodes_li = sibling_nodes_ul.xpath("./child::li")
        
        print(len(child_nodes_li))
