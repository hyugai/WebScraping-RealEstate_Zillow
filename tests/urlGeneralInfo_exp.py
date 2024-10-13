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
test_url = "https://www.zillow.com/albuquerque-nm/"
headers = {'User-Agent': random.choice(USER_AGENTS), 'Accept': ACCEPT,
           'Accept-Language': ACCEPT_LANGUAGE, 'Accept-Encoding': ACCEPT_ENCODING, 
           'Referer': REFERER}
with requests.Session() as s:
    r = s.get(test_url, headers=headers)
    if r.status_code == 200:
        dom = etree.HTML(str(BeautifulSoup(r.text, features='lxml').prettify()))
        nodes_script = dom.xpath("//script[@type='application/json']")
        script_content = nodes_script[-1].text
        substitutions = {r'true': 'True', r'false': 'False', 
                         r'null': 'None'}
        for sub in substitutions:
            script_content = re.compile(sub).sub(substitutions[sub], script_content)
        
        script_content: dict = eval(script_content.strip())
        
        # test: flatten the dict until meet the required keys
        key_to_find = 'listResults'
        while key_to_find not in script_content:
            tmp_dict = {}
            keys_to_keep = [tmp_dict.update(value) for value in script_content.values() if isinstance(value, dict)]
            script_content = tmp_dict
        
        homes = script_content[key_to_find]
        print(homes)
        ## test
    else:
        print(r.status_code)