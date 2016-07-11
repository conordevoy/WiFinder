import openpyxl
import csv
import os
import re

path_choice = '/home/mike/wifiproj/data' # local path, just to speed up script
os.chdir(path_choice)

wb = openpyxl.load_workbook('CSI Occupancy report.xlsx')
sheet = wb.get_sheet_by_name('CSI')

with open('CSI.csv', 'w') as f:
        c = csv.writer(f)
        for r in sheet.rows:
            c.writerow([cell.value for cell in r])

csi = open('CSI.csv')
csi_reader = csv.reader(csi)


csi_string = ''
for row in csi_reader:
    csi_string += ', '.join(row)
    csi_string += '\n'

    if 'Poor' in row: # stop 15000 lines of nothing
        break

mylist = []
match_list = []

mylist = csi_string.split('\n')

start_match = re.compile(r'CSI Classroom OCCUPANCY')
fin_match = re.compile(r'CSI Classroom UTILISATION')
blank_match = re.compile(r'^(, , , ,)')

start_flag = None
blank_flag = None

for row in mylist:
    if start_match.match(row): start_flag = True ; continue
    if fin_match.match(row): start_flag = False
    if blank_match.match(row): blank_flag = True

    if blank_flag:
        blank_flag = False
        continue

    if start_flag:
        match_list.append(row)

# for i in match_list:
#     print(i)

with open('CSI_clean.csv', 'w') as f:
        for item in match_list:
            f.writelines(item + '\n')