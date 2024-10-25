# libs
import os, sys
cwd = os.getcwd()
os.chdir('src'); path_to_src = os.getcwd()
os.chdir(cwd)
if path_to_src not in sys.path:
    sys.path.append(path_to_src)
from _libs import *
from _usr_libs import *

# exp
urls = [HOMEPAGE_URL]*100

def send_GETrequest(url: str):
    headers = {'Accept-Language': ACCEPT_LANGUAGE, 'Accept-Encoding': ACCEPT_ENCODING, 
               'User-Agent': UserAgent().random}
    with requests.Session() as s:
        r = s.get(url, headers=headers)
        if r.status_code == 200:
            pass
        else:
            pass

def get_numbersOfCPUs():
    print(mp.cpu_count())