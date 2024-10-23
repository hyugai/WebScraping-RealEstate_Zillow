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
#proxies = {'http': 'http://142.171.102.136:3128', 
#           'https': 'http://117.54.114.99:80'}
#headers = {'User-Agent': random.choice(USER_AGENTS), 'Accept-Encoding': ACCEPT_ENCODING, 
#           'Accept-Language': ACCEPT_LANGUAGE}
#with requests.Session() as s:
#    r = s.get(HOMEPAGE_URL, headers=headers, proxies=proxies)
#    if r.status_code != 200:
#        print(r.status_code)
#    else:
#        print(r.text)