import os
import shutil
import zipfile
import glob
import re
import pandas as pd

path_choice = '/home/mike/wifiproj'  # local path, just to speed up script
os.chdir(path_choice)

# copy data folder so's i don't fuck up the original

shutil.rmtree('/home/mike/wifiproj/new_data_test')
shutil.copytree('/home/mike/wifiproj/orig_data_test', '/home/mike/wifiproj/new_data_test')
os.chdir('/home/mike/wifiproj/new_data_test')

csi_zip = zipfile.ZipFile('CSI WiFiLogs.zip')
csi_zip.extractall('logzips')
os.chdir('logzips')


for each_zip in glob.glob("/home/mike/wifiproj/new_data_test/logzips/*.zip"):
    csi_zip = zipfile.ZipFile("{}".format(each_zip))
    csi_zip.extractall('logfiles')

os.chdir('logfiles')

test_file = "Client_Count_CSCI_B-02_20151102_213000_131.csv"
print test_file
df = pd.read_csv(test_file, skiprows=21)  # dangerous assumption
print df
# concat here

files = glob.glob("/home/mike/wifiproj/new_data_test/logzips/*.zip")
files = ' '.join(files)

pattern = re.compile(r'([A-Z]+_[a-zA-Z]-[0-9]+)')
rooms = set(pattern.findall(files))

print rooms

for room in rooms:
    os.mkdir(room)

# logfiles = glob.glob("/home/mike/wifiproj/new_data_test/logzips/*{}*.zip")

for room in rooms:
    print(os.getcwd())
    room_files = glob.glob("/home/mike/wifiproj/new_data_test/logzips/*{}*.zip".format(room))
    print(room_files)
    df = pd.read_csv(room_files[0], skiprows=21)
    df = pd.concat([pd.read_csv(room, skiprows=21) for room in room_files])
    df.to_csv("HELLO.csv".format(room))

# df = pd.concat([pd.read_csv(x, skiprows=21) for x in room_logs])
