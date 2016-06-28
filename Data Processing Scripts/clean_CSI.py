import csv
import pandas as pd
import re
import os

print(os.getcwd())
os.chdir('/home/mike/wifiproj/data')
print(os.getcwd())
data_xls = pd.read_excel('CSI Occupancy report.xlsx', 'CSI', index_col=None)
data_xls.to_csv('PDCSI.csv', encoding='utf-8')

lines = [line.strip() for line in open('PDCSI.csv')]
for x in lines:
    # print(x)
    # match=re.search(r'(?<=OCCUPANCY)(.*)(?=UTILISATION)',x)
    match=re.search(r'(OCCUPANCY)',x)
    if match: print(x)