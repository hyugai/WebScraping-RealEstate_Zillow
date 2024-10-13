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
test_url = "https://www.zillow.com/homedetails/1611-Los-Alamos-Ave-SW-Albuquerque-NM-87104/6710669_zpid/"
headers = {'User-Agent': random.choice(USER_AGENTS), 'Accept-Language': ACCEPT_LANGUAGE, 
           'Accept-Encoding': ACCEPT_ENCODING}
with requests.Session() as s:
    r = s.get(test_url, headers=headers)
    if r.status_code != 200:
        print(r.status_code)
    else:
        soup = BeautifulSoup(r.content.decode('utf-8'), features="lxml")
        dom = etree.HTML(str(soup))

    # test
    print(soup.prettify())
    ## test
