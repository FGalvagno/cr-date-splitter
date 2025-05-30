import pandas as pd
import os
from datetime import datetime, timedelta, date
from plotAWS import plot

class Splitter:
    """
    Initializes a Splitter object with the specified parameters.

    Args:
        src_loc (str): The source location where the input file is located.
        dest_loc (str): The destination location where the processed files will be stored.
        site (str): The site associated with the data.
        instrum (str): The instrument associated with the data.
        filename (str): The name of the input file.

    Attributes:
        cached_stamp (int): A timestamp used for tracking changes in the input file.
        src_loc (str): The source location where the input file is located.
        dest_loc (str): The destination location where the processed files will be stored.
        full_path (str): The full path to the input file.
        df (DataFrame): A Pandas DataFrame to store the data from the input file.
        site (str): The site associated with the data.
        instrum (str): The instrument associated with the data.
        filename (str): The name of the input file.
    """
    def __init__(self, src_loc, dest_loc, site, instrum, filename, plot):
        self._cached_stamp = 0
        self.src_loc = src_loc
        self.dest_loc = dest_loc
        self.full_path = src_loc + '/' + filename
        self.df = pd.DataFrame()
        self.site = site
        self.instrum = instrum
        self.filename = filename
        self.plot = plot


    def has_changed(self):
        """
        Checks if the file associated with the object has been modified since the last check.

        This method compares the modification timestamp (st_mtime) of the file at the specified path
        with the cached modification timestamp stored in the object. If the timestamps differ,
        it updates the cached timestamp and returns True indicating that the file has been modified.
        If the timestamps are the same, it returns False indicating that the file has not been modified.

        Returns:
            bool: True if the file has been modified since the last check, False otherwise.

        Raises:
            FileNotFoundError: If the file associated with the object does not exist.
            PermissionError: If the user does not have permission to access the file.

        Note:
            This method relies on the `os.stat()` function to retrieve the file's status.
        """
        stamp = os.stat(self.full_path).st_mtime
        if stamp != self._cached_stamp:
            self._cached_stamp = stamp
            return True
        return False
    
    def load_dat(self):
        """
        Reads a CSV file located at self.full_path, filters data for the current date,
        and stores it in self.df. Additionally, it saves the original header of the CSV file
        into self.hd.

        The function performs the following steps:
        1. Reads the CSV file located at self.full_path using pandas.read_csv().
        2. Skips the first, third, and fourth rows of the CSV file.
        3. Converts the 'TIMESTAMP' column to datetime format.
        4. Filters data for the current date.
        5. Stores the filtered data in self.df.
        6. Saves the first four rows of the original CSV file into self.hd.

        Note:
            - This function assumes that self.full_path points to a valid CSV file.
            - The 'TIMESTAMP' column is expected to exist in the CSV file.
        """

        # read file
        # print("Reading file " + self.src_loc +'/'+ self.filename )
        df = pd.read_csv(self.full_path, skiprows=[0, 2, 3])
        # print(df)
        df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'])
        i = date.today()
        self.df = df[(df['TIMESTAMP'].dt.date >= i) & (df['TIMESTAMP'].dt.date < i+timedelta(days=1))]
        
        #save original header
        with open(self.full_path) as input_file:
            self.hd = [next(input_file) for _ in range(4)]

    def split_date(self):
        """
        Updates or creates a CSV file containing data stored in self.df at the destination specified by self.dest_loc,
        organized by instrument, site, and date.

        The function performs the following steps:
        1. Constructs the file_path using the current date and other attributes of the object.
        2. Creates the directory structure if it doesn't already exist.
        3. Checks if the file_path exists.
        4. If the file exists:
            a. Saves the contents of self.df into a temporary file ("temp") excluding the header.
            b. Compares the lines in "temp" with the existing file (excluding the header) and appends
           any new lines to the existing file.
            c. Removes the temporary file.
        5. If the file doesn't exist:
            a. Writes the header (stored in self.hd) to the file.
            b. Appends the contents of self.df to the file.

        Note:
             This function assumes that self.df contains data to be written to the CSV file.
            - It assumes self.dest_loc is a valid directory path.
            - The constructed file_path is based on the current date and other attributes of the object.
        """

        i = date.today()
        file_path = self.dest_loc + "/" +self.instrum + f"/{i.strftime('/%Y/%m/'+ self.site + '_' +  self.instrum + '_' +'%Y-%m-%d')}.csv" 
       
        if not os.path.exists(self.dest_loc + '/' + self.instrum + f"/{i.strftime('/%Y/%m')}"):
            os.makedirs(self.dest_loc + '/' + self.instrum + f"/{i.strftime('/%Y/%m')}")
        
        if(os.path.isfile(file_path)):
            self.df.to_csv("temp", index=False, mode = 'w', header=False)
            with open(file_path, 'r') as t1, open('temp', 'r') as t2:
                fileone = t1.readlines()[4:]
                filetwo = t2.readlines()
            with open(file_path, 'a') as outFile:
                for line in filetwo:
                    if line not in fileone:
                        outFile.write(line)
                        print(line)
            os.remove("temp")
            
        else:
            with open(file_path, 'w') as f:
                f.writelines(self.hd)
                f.close()
                print(self.hd)
            print(self.df)
            self.df.to_csv(file_path, index=False, mode = 'a', header=False)

        if self.plot:
            try:
                plot(file_path, self.site)
            except Exception as e:
                print(f"Error plotting data for {self.site}: {e}")
