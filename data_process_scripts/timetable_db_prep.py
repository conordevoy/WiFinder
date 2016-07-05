
# coding: utf-8

import pandas as pd
import os

os.chdir('/home/mike/wifiproj/data')

timetables = ['B0.02_ready', 'B0.03_ready', 'B0.04_ready']
cleantables = []


for timetable in timetables:

    df = pd.read_csv('{}.csv'.format(timetable))

    df = df.ix[:9, :11]



    mon_df = pd.DataFrame(index = range(10), columns=['Time', 'Date', 'Room', 'Room_Capacity', 'Module', 'Registered_Students'])

    tue_df = pd.DataFrame(index = range(10), columns=['Time', 'Date', 'Room', 'Room_Capacity', 'Module', 'Registered_Students'])

    wed_df = pd.DataFrame(index = range(10), columns=['Time', 'Date', 'Room', 'Room_Capacity', 'Module', 'Registered_Students'])

    thu_df = pd.DataFrame(index = range(10), columns=['Time', 'Date', 'Room', 'Room_Capacity', 'Module', 'Registered_Students'])

    fri_df = pd.DataFrame(index = range(10), columns=['Time', 'Date', 'Room', 'Room_Capacity', 'Module', 'Registered_Students'])

    day_tables = [mon_df, tue_df, wed_df, thu_df, fri_df]


    n = 1

    for table in day_tables:
        table.Time = df[[0]].ix[1:]
        table.Module = df[[n]].ix[1:]
        table.Registered_Students = df[[n+1]].ix[1:]
        room = df.columns[0]
        csroom = 'CS' + room
        table.Room= csroom
        table.Room_Capacity = df.columns[2].split(' ')[2]
        # date. changeable
        n += 2

    del n


    df = pd.concat(day_tables)

    df = df[df.Time.notnull()]

    two_weeks = [df, df]

    df = pd.concat(two_weeks)

    date_index = pd.date_range('2015-11-2', periods=12, freq='D')


    day = 0
    count = 0

    while count < df.shape[0]:
        df.iat[count,1] = date_index[day]

        if (count + 1)% 9 == 0:
            day += 1

            if day == 5:
                day += 2

        count += 1

    count = 0

    while count < df.shape[0]:
        if pd.isnull(df.iat[count,4]):
            df.iat[count,4] = 'Vacant'
            df.iat[count,5] = 'Vacant'

        count += 1

    print df

    cleantables.append(df)

df.reset_index(drop=True)

df_finish = pd.concat(cleantables)
print df_finish

df_finish.to_csv('timetable_table.csv')

roomtable = df[['Room', 'Room_Capacity']]
modtable = df[['Module', 'Registered_Students']]

roomtable.to_csv('room_table.csv')
modtable.to_csv('mod_table.csv')