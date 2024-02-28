import os
import time
from datetime import datetime
import glob

import yaml

from splitter import Splitter




def main():
    if not os.path.exists('export'):
        os.makedirs('export')
    s = []
    #f = open("config/AWS.yml", 'r')
    #cfg = yaml.safe_load(f)

    cfg_files = glob.glob('./config/*.yml')

    for cfg in cfg_files:
        s.append(
            Splitter(
            cfg["path"]["src"],
            cfg["path"]["dest"], 
            cfg["site"],
            cfg["instrum"], 
            cfg["file_name"])
        )

    while(True):
        for splitter in s:
            if(splitter.has_changed()):
                print("Processing changes: ", datetime.now())
                splitter.load_dat()
                splitter.split_date()    
        time.sleep(30)
        


if __name__ == "__main__":
    main()