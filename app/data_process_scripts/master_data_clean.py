import os
import sys
import data_process_scripts.straight_line_timetable


def check_path():

    print('The current working directory is:', os.getcwd())
    path = input('To use another directory, please press any key followed by enter. Otherwise, just press enter. ')


    if path != '':
        path_choice = input('Please enter the directory to use: \n')
        invalid_path = True

        while invalid_path:
            try:
                os.chdir(path_choice)
                invalid_path = False
            except:
                path_choice = input('Invalid path. Please enter the directory to use: \n')

check_path()

ttxl.
