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

async def fetch(session: aiohttp.ClientSession, url: str):
    async with session.get(url) as r:
        print(f"Status: {r.status}")
        await r.text

async def main():
   #queue = asyncio.Queue() 
   async with aiohttp.ClientSession() as session:
       pass