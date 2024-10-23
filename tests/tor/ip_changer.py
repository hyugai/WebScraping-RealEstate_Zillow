# libs
import os, sys
cwd = os.getcwd()
os.chdir('src/'); path_to_src = os.getcwd()
os.chdir(cwd)
if path_to_src not in sys.path:
    sys.path.append(path_to_src)

from _libs import *
from _usr_libs import *

## original ip
#with requests.Session() as s:
#    r = s.get('https://ident.me')
#    if r.status_code != 200:
#        print(f'Error {r.status_code}: {r.text}')
#    else:
#        print(r.text)
#
## using tor to change ip
proxies = {'http': 'socks5://127.0.0.1:9050',
           'https': 'socks5://127.0.0.1:9050'} 
#           
#with requests.Session() as s:
#    r = s.get('https://ident.me', proxies=proxies)
#    if r.status_code != 200:
#        print(f'Error {r.status_code}: {r.text}')
#    else:
#        print(r.text)

# change user-agent and ip every 10s
num_iters = range(3)
for _ in num_iters:
    headers = {'User-Agent': UserAgent().random}
    time.sleep(10)
    
    with Controller.from_port(port=9051) as c:
        c.authenticate('zillow')
        c.signal(Signal.NEWNYM)
        print(f"{requests.get('https://ident.me', headers=headers, proxies=proxies).text} || {headers['User-Agent']}")