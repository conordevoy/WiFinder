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

results = []

filelist = glob.glob(os.path.join('*.csv'))
for infile in sorted(filelist):

	f = open(infile, 'rt')
	try:
		reader = csv.reader(f)
		for row in reader:
			if re.search(r'\bBelfield\b',row[0]):
				results.append(row)
	finally:
		f.close()

with open('results.csv', 'w') as f:
	writer = csv.writer(f)
	writer.writerows(results)
