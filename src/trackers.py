# libs
from libs import *

# TableTracker
class TableTracker():
    def __init__(self, 
                 path: str, name: str):
        self.path = path
        self.name = name

    def create(self, 
               columns: tuple[str], uniq: str):
        with sqlite3.connect(self.path) as conn:
            cur = conn.cursor()
            cur.execute(f"CREATE TABLE IF NOT EXISTS {self.name} {columns}, UNIQUE ({uniq}))")
    
    def insert(self, 
               columns: tuple[str], values: tuple):
        with sqlite3.connect(self.path) as conn:
            cur = conn.cursor()
            cur.execute(f"INSERT OR REPLACE INTO {self.name} {columns} VALUES {values}")