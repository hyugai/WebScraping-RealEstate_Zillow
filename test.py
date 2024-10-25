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
proxies = {'http': 'socks5h://localhost:9050', 
           'https': 'socks5h://localhost:9050'}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36', 
           'Accept-Encoding': ACCEPT_ENCODING, 'Accept-Language': ACCEPT_LANGUAGE}
with Controller.from_port(port=9051) as c:
    c.authenticate('zillow')
    c.signal(Signal.NEWNYM)
    with requests.Session() as s:
        r = s.get(HOMEPAGE_URL, headers=headers)
        if r.status_code != 200:
           print(r.text) 
        else:
            print(r.status_code)
