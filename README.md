# Campbell Date Splitter

## Description
A python program to daily split the data from Campbell CR series dataloggers. 

The data files are splitted on the go, so a previous dates backup must be done before setting up this script.

The program supports multiple files (or tables, defined by "instrument name" and "file name"). Since the program is made to be running on backround, a tray icon is showed.

## Installation
Clone the repository: 
```
git clone https://github.com/FGalvagno/cr-date-splitter.git
```

Install dependencies: 
```
pip install -r requirements.txt
```

__Warning:__ if the script is running on Windows 7 or below, you may have to install dependencies manually: _numpy, pandas, pillow, pystray, python-dateutil, python-xlib, pytz, PyYAML, six, tzdata._

## Usage
Create YAML configuration files in _/config_ folder:
```YAML
path: 
      src: "./"         #path of data src e.g: "C:/COR_PASIVOS COR_AWS-DATOS"
      dest: "./export"  #dest path of exported files

site: "COR" 
#-----SITE INFO-----#
#locations:
#"PIL" or "COR" 
#"TUC"
#"VM or "CITEDEF"
#"SMN"
#"NQN"
#"BRC"
#"TRW"
#"CRD"
#"RGL"

#-----INSTRUM INFO-----#
#instrum: "RAD" or "AWS"
instrum: "RAD"

file_name: "COR_AWS.dat" #name of src file e.g: "COR_AWS.dat"

```
It's necessary to create one config file per instrument/data table.

## Files and Directories
By default, all the output data goes into _export_ folder, located on the root. It can be changed by editing the config parameter _dest_ 

