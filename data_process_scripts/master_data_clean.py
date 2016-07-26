import os
from data_process_scripts.straight_line_timetable import clean_tables
from data_process_scripts.timetable_db_prep import timetables_to_csv
from data_process_scripts.log_file_cleaner import clean_log_files
from data_process_scripts.csi_Test import clean_CSI_csv_files
from data_process_scripts.CSI_db_formatting import prep_CSI_db_files




def check_path():

    print('The current working directory is:', os.getcwd())
    path = input('If this is correct, press enter now. \n'
                 'Otherwise, press any key followed by enter.\n')


    if path != '':
        path_choice = input('Please enter the directory to use: \n')
        invalid_path = True

        while invalid_path:
            try:
                os.chdir(path_choice)
                invalid_path = False
            except:
                path_choice = input('Invalid path. Please enter the directory to use: \n')

    return path_choice

check_path()
path_choice = os.getcwd()

# clean the timetables

clean_tables()

timetables_to_csv()

# clean the log files

clean_log_files(path_choice)

# clean the survey data

clean_CSI_csv_files()

prep_CSI_db_files()

