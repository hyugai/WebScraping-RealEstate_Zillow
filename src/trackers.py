# libs
from _libs import *

# class url tracker
class TableTracker():
    def __init__(self, 
                 db_path: str, table_name: str) -> None:
        self.db_path = db_path
        self.table_name = table_name

    def create(self, 
               uniq_column: str, all_columns: tuple[str]) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name}({uniq_column} TEXT UNIQUE)")
            
            cur.execute(f"PRAGMA table_info({self.table_name})")
            columns = cur.fetchall()
            existing_names = [column[1] for column in columns]

            for name in all_columns:
                if name not in existing_names:
                    cur.execute(f"ALTER TABLE {self.table_name} ADD COLUMN {name}")
                else:
                    continue
            
            cur.close()

    def insert(self, 
               columns: tuple[str], 
               row: tuple) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(f"INSERT OR REPLACE INTO {self.table_name}{columns} VALUES{row}")

            cur.close()

    def retrieve(self, 
                 columns: tuple[str]) -> list[tuple]:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT {columns} FROM {self.table_name}")
            
            rows = cur.fetchall()
            if rows:
                return rows
            else:
                raise Exception("Table is EMPTY!!!")

# class json tracker
class JSONTracker():
    def __init__(self):
        pass