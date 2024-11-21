# libs
from usr_libs import *

# class DataReport
class DataReport():
    def __init__(self, 
                 csv_path: str, report_path: str, 
                 report_title: str)-> None:
        self.df = pd.read_csv(csv_path) 
        self.report_path = report_path 
        self.report_title = report_title

    def generate(self):
        buffer = StringIO()
        self.df.info(buf=buffer)

        print(f"{self.report_title.upper()}\
              \nShape: {self.df.shape}\
              \nHead: \n{tabulate(self.df.head(), headers='keys', tablefmt='psql')}\
              \nTail: \n{tabulate(self.df.tail(), headers='keys', tablefmt='psql')}\
              \nInfo: \n{buffer.getvalue()}", file=self.report_path) 