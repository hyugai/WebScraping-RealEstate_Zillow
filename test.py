# libs
import os, sys
cwd = os.getcwd()
os.chdir('src'); path_to_src = os.getcwd()
os.chdir(cwd)
if path_to_src not in sys.path:
    sys.path.append(path_to_src)
from libs import *
with requests.Session() as s:
    r = s.get(ZILLOW, headers={'User-Agent': UserAgent().random})
    if r.status_code == 200:
        print(r.text)
    else:
        print(r.status_code)