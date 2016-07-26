import os
import shutil
import zipfile
import glob
import re
import csv

path_choice = '/home/devcon90/RPData/test'
os.chdir(path_choice)

shutil.rmtree('/home/devcon90/RPData/test/new_data')
shutil.copytree('/home/devcon90/RPData/test/original_data', '/home/devcon90/RPData/test/new_data')
os.chdir('/home/devcon90/RPData/test/new_data')

csi_zip = zipfile.ZipFile('CSIWiFiLogs.zip')
csi_zip.extractall('logzips')
os.chdir('/home/devcon90/RPData/test/new_data/logzips')

for each_zip in glob.glob("/home/devcon90/RPData/test/new_data/logzips/*.zip"):
    csi_zip = zipfile.ZipFile("{}".format(each_zip))
    csi_zip.extractall('/home/devcon90/RPData/test/new_data/logfiles')

os.chdir('/home/devcon90/RPData/test/new_data/logfiles')

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

with open('results.csv', 'w') as f:
	writer = csv.writer(f)
	writer.writerows(results) # dump the results list to a new results file
