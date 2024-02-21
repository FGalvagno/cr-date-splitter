import json
from splitter import Splitter
import os
import time

f = open("config/AWS.json")
cfg = json.load(f)

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
            print("Processing...")
            s1.load_dat()
            s1.split_date()
        else:
            print("File has not changed")
        time.sleep(10)
        


if __name__ == "__main__":
    main()