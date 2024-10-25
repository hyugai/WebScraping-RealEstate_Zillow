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
urls = [HOMEPAGE_URL]*5

def send_GETrequest(url: str):
    headers = {'Accept-Language': ACCEPT_LANGUAGE, 'Accept-Encoding': ACCEPT_ENCODING, 
               'User-Agent': UserAgent().random}
    with requests.Session() as s:
        r = s.get(url, headers=headers)
        if r.status_code == 200:
            print('Succeeded')
        else:
            print('Failed') 

def parallel_requets():
    with mp.Pool(processes=2) as pool:
        pool.map(send_GETrequest, urls)

def get_numbersOfCPUs():
    print(mp.cpu_count())

if __name__ == '__main__':
    start = time.time()
    parallel_requets()
    print(f"Duration: {time.time() - start}")
    
    start = time.time()
    for url in urls:
        send_GETrequest(url)
    print(f"Duration: {time.time() - start}")