import os
import shutil
import zipfile
import glob
import re
import pandas as pd

path_choice = input("Please enter the directory to work from: ")
path_choice = '/home/mike/wifiproj'  # local path, just to speed up script
os.chdir(path_choice)

# copy data folder so's i don't fuck up the original

# enter name of data folder here so it copies it and modifies the copy
# datafolder = 'orig_data_test'
# shutil.rmtree('{}{}{}'.format(path_choice, '/', datafolder))
shutil.rmtree('/home/mike/wifiproj/new_data_test')
shutil.copytree('/home/mike/wifiproj/orig_data_test', '/home/mike/wifiproj/new_data_test')
os.chdir('/home/mike/wifiproj/new_data_test')


csi_zip = zipfile.ZipFile('CSI WiFiLogs.zip') # select first zip file
csi_zip.extractall('logzips') # extrac contents of zip and place them in new folder 'logzips'
os.chdir('logzips') # change to that directory

# globs select all files that fit a pattern
# below it's the pattern that: they are in a directory '.../logzips/'
# and the files end in .zip
for each_zip in glob.glob("/home/mike/wifiproj/new_data_test/logzips/*.zip"):
    csi_zip = zipfile.ZipFile("{}".format(each_zip)) # select each zip file in turn
    csi_zip.extractall('logfiles') # extract its contents to 'logfiles' folder
    # only creates folder first time

os.chdir('logfiles') # switch to logfiles folder

# all this below is testing - trying to select each room's .csvs in turn


files = glob.glob("/home/mike/wifiproj/new_data_test/logzips/*.zip")
files = ' '.join(files)

pattern = re.compile(r'([A-Z]+_[a-zA-Z]-[0-9]+)') # creates a regex pattern
rooms = set(pattern.findall(files)) # creates a set of everything matching that pattern
# this matches the room names

print(rooms) # print all the room names found

for room in rooms: # make a folder for each room's files
    os.mkdir(room)

for room in rooms: # for each room title
    room_files = glob.glob(os.getcwd() + "*{}*.csv".format(room)) # glob all that rooms .csvs
    print(room_files) # check to see what's in them
    destination = os.getcwd() + '/' + room # create the destination folder name
    print(destination) # check that
    for each_file in room_files: # for each csv, move to that folder
        shutil.move(each_file, destination)

# above code won't catch csvs. no idea why. it catches zips and other things fine.