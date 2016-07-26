
# coding: utf-8

import pandas as pd
import os
import glob

def timetables_to_csv():

    directory = os.getcwd()

    timetables = glob.glob(directory + '/' + '*_ready.csv') # finds all files ending in _ready.csv

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
            table.Time = df[[0]].ix[1:]
            table.Module = df[[column]].ix[1:]
            table.Registered_Students = df[[column+1]].ix[1:]
            room = df.columns[0]
            csroom = 'CS' + room
            table.Room = csroom
            table.Room_Capacity = df.columns[2].split(' ')[2]
            # date. changeable
            column += 2

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

     #  MAYBE REMOVE THESE BECAUSE THEY'RE STUPID AND REDUNDANT
    for row in range(df_finish.shape[0]):
        room_value = str(df_finish.iat[row, 2])
        room_value.replace('.', '')
        room_value.replace('CS', '')
        df_finish.iat[row, 2] = room_value

    df_finish.reset_index(drop=True) # reset the index of the joined tables

    #keep only first two characters in Time
    for item, frame in df_finish['Time'].iteritems():
        df_finish['Time'] = df_finish['Time'].map(lambda x: str(x)[:2])

    #remove : from time
    for item, frame in df_finish['Time'].iteritems():
        df_finish['Time'] = df_finish['Time'].map(lambda x: x.lstrip(':').rstrip(':'))

    #retain only first 10 characters in date
    for item, frame in df_finish['Date'].iteritems():
        df_finish['Date'] = df_finish['Date'].map(lambda x: str(x)[:10])

    df_finish.to_csv('timetable_table.csv', index=False) # convert df to .csv, drop the index

    roomtable = df[['Room', 'Room_Capacity']] # create table according to DB schema
    modtable = df[['Module', 'Registered_Students']] # create table according to DB schema

    roomtable.to_csv('room_table.csv', index=False) # convert df to .csv, drop the index
    modtable.to_csv('mod_table.csv', index=False) # convert df to .csv, drop the index

    classtable = df[['Room', 'Module', 'Date', 'Time']] # create table according to DB schema
    classtable.to_csv('class_table.csv', index=False) # convert df to .csv, drop the index
