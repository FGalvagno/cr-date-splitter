import json
from splitter import Splitter
import os
import time

def main():
    if not os.path.exists('export'):
        os.makedirs('export')

    s1 = Splitter("./","export", "COR", "AWS", "COR_AWS.dat")


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