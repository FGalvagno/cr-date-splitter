import pandas as pd
import os
from datetime import datetime, timedelta, date

class Splitter:
    def __init__(self, src_loc, dest_loc, site, instrum, filename):
        self._cached_stamp = 0
        self.src_loc = src_loc
        self.dest_loc = dest_loc
        self.df = pd.DataFrame()
        self.site = site
        self.instrum = instrum
        self.filename = filename

    def has_changed(self):
        stamp = os.stat(self.filename).st_mtime
        if stamp != self._cached_stamp:
            self._cached_stamp = stamp
            return True
        return False
    
    def load_dat(self):
        # read file
        df = pd.read_csv(self.src_loc + self.filename, skiprows=[0, 2, 3])
        print(df)
        df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'], format='mixed')
        i = date.today()
        self.df = df[(df['TIMESTAMP'].dt.date >= i) & (df['TIMESTAMP'].dt.date < i+timedelta(days=1))]



    def split_date(self):
        i = date.today()
        file_path = self.dest_loc + "/" +self.instrum + f"/{i.strftime('/%Y/%m/'+ self.site +'-%Y-%m-%d')}.csv" 
       
        if not os.path.exists(self.dest_loc + '/' + self.instrum + f"/{i.strftime('/%Y/%m')}"):
            os.makedirs(self.dest_loc + '/' + self.instrum + f"/{i.strftime('/%Y/%m')}")
        
        if(os.path.isfile(file_path)):
            self.df.to_csv("temp", index=False, mode = 'w', header=False)
            with open(file_path, 'r') as t1, open('temp', 'r') as t2:
                fileone = t1.readlines()
                filetwo = t2.readlines()
            with open(file_path, 'a') as outFile:
                for line in filetwo:
                    if line not in fileone:
                        outFile.write(line)

        else:
            self.df.to_csv(file_path, index=False, mode = 'w', header=False)
