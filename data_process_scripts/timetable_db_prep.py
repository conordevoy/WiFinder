# %load timetable_db_prep.py

import pandas as pd
import os
import glob

directory = input("Please enter location of the timetable csv files: ")
# os.chdir('/home/mike/wifiproj/data') # change to directory where file is located

os.chdir(directory)

timetables = glob.glob(directory + '/' + '*_ready.csv') # finds all files ending in _ready.csv
for t in timetables:
    print(t) # check to ensure only desired files are matched

cleantables = [] # make new list to store the names of cleaned tables;
                # this is needed for using pd.concat later on to join them end to end


for timetable in timetables:

    df = pd.read_csv('{}'.format(timetable)) # read the timetable

    df = df.ix[:9, :11] # cut out unneeded rows and columns
                        # not flexible; what if the structure changes?
                        # could be replaced with regex or something; not sure


# make the dataframes for each day; all identical

    mon_df = pd.DataFrame(index = range(10), columns=['Time', 'Date', 'Room', 'Room_Capacity', 'Module', 'Registered_Students'])

    tue_df = pd.DataFrame(index = range(10), columns=['Time', 'Date', 'Room', 'Room_Capacity', 'Module', 'Registered_Students'])

    wed_df = pd.DataFrame(index = range(10), columns=['Time', 'Date', 'Room', 'Room_Capacity', 'Module', 'Registered_Students'])

    thu_df = pd.DataFrame(index = range(10), columns=['Time', 'Date', 'Room', 'Room_Capacity', 'Module', 'Registered_Students'])

    fri_df = pd.DataFrame(index = range(10), columns=['Time', 'Date', 'Room', 'Room_Capacity', 'Module', 'Registered_Students'])


    # make list to use pd.concat
    day_tables = [mon_df, tue_df, wed_df, thu_df, fri_df]


    column = 1 # counter for controlling the column to take values from

    for table in day_tables:
        table.Time = df[[0]].ix[1:] # pull the time values; same for all tables
        table.Module = df[[column]].ix[1:] # pull the modules from the given column
        table.Registered_Students = df[[column+1]].ix[1:] # pull corresponding students, from column+1
        room = df.columns[0] # room is the same for each timetable
        csroom = 'CS' + room # append 'CS' as identifier for room
        table.Room= csroom # room = the appended string, e.g. 'CSB002'
        table.Room_Capacity = df.columns[2].split(' ')[2] # pull room capacity from  existing string 'room capacity: 90'
        column += 2 # increment column by 2 as modules and students come in sets of 2 columns.

    del column # clean column for subsequent loops


    df = pd.concat(day_tables) # join all daytables into one dataframe

    df = df[df.Time.notnull()] # remove any rows where there is no time value

    two_weeks = [df, df] # make list to duplicate timetable for second week

    df = pd.concat(two_weeks) # join these together

    date_index = pd.date_range('2015-11-2', periods=12, freq='D') # create date range


    # this loop assigns every row a date
    day = 0
    count = 0

    while count < df.shape[0]: # while less than no. of rows
        df.iat[count,1] = date_index[day] #

        if (count + 1)% 9 == 0:     # every nine rows, increment the day
            day += 1                # assumes 9 timeslots per day (9 - 17)

            if day == 5:            # skip the weekend days once you hit friday
                day += 2            # error if: not scalable to longer than two weeks

        count += 1

    # this loop assigns a value to 'module' and 'registered_students' if 'module' == NaN
    # error: doesn't modify for some modules that don't have registered students
    # see B004, leaves some 'reg_students' columns as NaN
    count = 0

    while count < df.shape[0]:
        if pd.isnull(df.iat[count,4]): # if module value is NaN
            df.iat[count,4] = 'Vacant'
            df.iat[count,5] = '-1'

        count += 1

    cleantables.append(df) # append this df to clean_tables; needed for pd.concat


df_finish = pd.concat(cleantables)
df_finish.reset_index(drop=True) # reset the index of the joined tables

#call the function to strip the data
strip_data(df_finish)

#rename columns
df_finish.columns = ['Hour', 'Date', 'Room', 'Room_Capacity', 'Module', 'Registered_Students']
#create an empty ID column and call function to ceate unique ID for each row
df_finish['ID'] = ""
set_identifier(df_finish)
#save as csv
df_finish.to_csv('/Users/shauna/Desktop/Wifinder/WiFinder/Data/final_csvs/timetable_table.csv', index=False)

roomtable = df[['Room', 'Room_Capacity']] # create table according to DB schema
modtable = df[['Module', 'Registered_Students']] # create table according to DB schema

roomtable.to_csv('room_table.csv', index=False) # convert df to .csv, drop the index
modtable.to_csv('mod_table.csv', index=False) # convert df to .csv, drop the index

classtable = df[['Room', 'Module', 'Date', 'Time']] # create table according to DB schema
classtable.to_csv('class_table.csv', index=False) # convert df to .csv, drop the index

