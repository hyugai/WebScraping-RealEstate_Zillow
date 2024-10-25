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
headers = {'Accept-Language': ACCEPT_LANGUAGE, 'Accept-Encoding': ACCEPT_ENCODING}
ip_tracker = IPTracker(CONTROL_PORT_PASSWD, CONTROL_PORT, PROXIES, headers)

url = "http://httpbin.org/ip"
text = ip_tracker.send_GETrequest(url, 5)
print(text)