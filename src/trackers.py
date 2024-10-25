# libs
from _libs import *

# class logs tracker
class LogsTracker():
    def __init__(self):
        pass
# class IP tracker
class IPTracker():
    def __init__(self, 
                 ctrlPort_passwd: str, ctrlPort: int, 
                 proxies: dict, headers: dict) -> None:

       self.proxies = proxies
       self.ctrlPort_passwd = ctrlPort_passwd
       self.ctrlPort = ctrlPort
       self.headers = headers

    def change_IP(self) -> None:
        with Controller.from_port(port=self.ctrlPort) as c:
            c.authenticate(self.ctrlPort_passwd)
            c.signal(Signal.NEWNYM)

    def send_GETrequest(self, 
                        url: str, num_trials: int) -> str:
        trial = 1 
        while trial <= num_trials:
            # send request
            with requests.Session() as s:
                r = s.get(url=url, headers=self.headers) 
                if r.status_code == 200:
                    print(f'Trial {trial}: Succeeded')
                    return r.text 
                else:
                    print(f'Trial {trial}: Failed')
                    trial += 1
                    continue
        
        raise ValueError("Fail to retrive HTML!")

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
                 columns: list[str]) -> list[tuple]:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT {', '.join(columns)} FROM {self.table_name}")
            
            rows = cur.fetchall()
            if rows:
                return rows
            else:
                raise Exception("Table is EMPTY!!!")

# class json tracker
class JSONTracker():
    def __init__(self):
        pass