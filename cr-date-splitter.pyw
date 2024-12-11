import os
import time
from datetime import datetime
import glob

import pystray
import PIL.Image
import yaml

from splitter import Splitter

debug = True

if not 'PROMPT' in os.environ and debug:
    import sys
    nullfile = open(os.devnull, 'w')
    sys.stdout = nullfile
    sys.stderr = nullfile


## image for tray icon 
image = PIL.Image.open("./img/icon.png")

## define tray function
def on_clicked(icon, item):
    if str(item) == "Exit":
        icon.stop()
        os._exit(1)

icon = pystray.Icon("CR Splitter", image, menu=pystray.Menu(
    pystray.MenuItem("Exit", on_clicked)

))

## main process
def main():
    icon.run_detached()
    
    ## check for basic export folder
    if not os.path.exists('export'):
        os.makedirs('export')
    
    s = []
    config = []

    ## create an array of splitters, based on .yml config files.
    cfg_files = glob.glob('./config/*.yml')
    for file in cfg_files:
        f = open(file,'r')
        config.append(yaml.safe_load(f))

    for cfg in config:
        s.append(
            Splitter(
            cfg["path"]["src"],
            cfg["path"]["dest"], 
            cfg["site"],
            cfg["instrum"], 
            cfg["file_name"])
        )

    ## check for changes in files with polling.
    while(True):
        for splitter in s:
            if(splitter.has_changed()):
                print("Processing changes: ", datetime.now())
                splitter.load_dat()
                splitter.split_date()    
        time.sleep(30)

if __name__ == "__main__":
    main()
