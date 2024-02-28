import yaml
import os
import time
from datetime import datetime

from splitter import Splitter

f = open("config/AWS.yaml", 'r')
cfg = yaml.safe_load(f)

def main():
    if not os.path.exists('export'):
        os.makedirs('export')

    s1 = Splitter(
        cfg["path"]["src"],
        cfg["path"]["dest"], 
        cfg["site"],
        cfg["instrum"], 
        cfg["file_name"])


    while(True):
        if(s1.has_changed()):
            print("Processing changes: ", datetime.now())
            s1.load_dat()
            s1.split_date()
        time.sleep(30)
        


if __name__ == "__main__":
    main()