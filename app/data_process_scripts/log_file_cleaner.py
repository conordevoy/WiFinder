import os
import zipfile
import glob
import re
import csv


def clean_log_files(path_choice):


    csi_zip = zipfile.ZipFile('CSI WiFiLogs.zip')
    csi_zip.extractall('logzips')
    os.chdir('logzips')

    for each_zip in glob.glob("*.zip"):
        csi_zip = zipfile.ZipFile("{}".format(each_zip))
        csi_zip.extractall(path_choice + '/' + 'logfiles')

    os.chdir(path_choice + '/' + 'logfiles')

    # All Mikes code upto now

    results = [] # list to hold the results of the regex magic to be run on each file

    filelist = glob.glob(os.path.join('*.csv')) # had to do this to keep the files in order
    for infile in sorted(filelist): # sorted as in directory

        f = open(infile, 'rt') # opens each file
        try:
            reader = csv.reader(f)
            for row in reader:
                if re.search(r'\bBelfield\b',row[0]): # regex to find rows begining with the word Belfield
                    results.append(row) # appends said rows to list
        finally:
            f.close() # closes each file, so that the next one can be opened using the same process

    os.chdir(path_choice)

    with open('log_files_cleaned.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(results) # dump the results list to a new results file
