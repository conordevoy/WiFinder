import openpyxl
import csv
import re


def clean_CSI_csv_files():

    wb = openpyxl.load_workbook('CSI Occupancy report.xlsx') # load correct workbook
    sheet = wb.get_sheet_by_name('CSI') # pull CSI sheet as it is the only important one

    # create CSI.csv file, and iterate through each row, writing the cell value into the new csv
    with open('CSI.csv', 'w') as f:
            c = csv.writer(f)
            for r in sheet.rows:
                c.writerow([cell.value for cell in r])

    csi = open('CSI.csv') # open new .csv file
    csi_reader = csv.reader(csi) # create reader object


    csi_string = '' # create empty string for storing elements of csv
    for row in csi_reader:
        csi_string += ', '.join(row) # join each row's elements with a comma and a space
        csi_string += '\n' # join each line with a newline to maintain original structure

        if 'Poor' in row: # stop 15000 lines of nothing
            break

    csi_row_list = []
    match_list = []

    csi_row_list = csi_string.split('\n')

    # create regex match patterns
    start_match = re.compile(r'CSI Classroom OCCUPANCY') # for matching start of relevant block
    fin_match = re.compile(r'CSI Classroom UTILISATION') # for matching end of relevant block
    blank_match = re.compile(r'^(, , , ,)') # for matching blank lines

    start_flag = None # tracks when in relevant block
    blank_flag = None # tracks if blank row detected

    for row in csi_row_list:
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