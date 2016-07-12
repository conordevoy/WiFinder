import os
import csv
import re

os.chdir('/home/devcon90/WiFinder/Data')

results = []

f = open('results.csv', 'rt')
try:
	reader = csv.reader(f)
	for row in reader:
		if re.search(r'\bB-002\b',row[0]):
			row.append('Belfield')
			row.append('Computer Science')
			row.append('B002')
		elif re.search(r'\bB-003\b',row[0]):
			row.append('Belfield')
			row.append('Computer Science')
			row.append('B003')
		else:
			row.append('Belfield')
			row.append('Computer Science')
			row.append('B004')
		row.append(row[1][4:7]) # date month
		row.append(row[1][8:10]) # date day
		row.append(row[1][11:19]) # time(24 hour clock)
		row.append(row[1][11:13]) # hour
		results.append(row)
finally:
	f.close()

# print(results)

with open('clean_log_results.csv', 'w') as f:
	writer = csv.writer(f)
	writer.writerows(results)