# libs
from _libs import *

# class url tracker
class URLTracker():
    def __init__(self, 
                 db_path: str, table_name: str) -> None:
        self.db_path = db_path
        self.table_name = table_name

    def create(self, 
               uniq_column: str, others: list[str]) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name}({uniq_column} TEXT UNIQUE)")
            
            cur.execute(f"PRAGMA table_info({self.table_name})")
            columns = cur.fetchall()
            existing_names = [column[1] for column in columns]

            for name in others:
                if name not in existing_names:
                    cur.execute(f"ALTER TABLE {self.table_name} ADD COLUMN {name}")
                else:
                    continue

    def insert(self, 
               columns: tuple[str], 
               row: tuple) -> None:
        pass

    def retrieve(self):
        pass