
# coding: utf-8



import pandas as pd


df = pd.read_csv('B002_finalmerge.csv')

df2 = df.ix[:9, :11]

del df



mon_df = pd.DataFrame(index = range(10), columns=['Time', 'Date', 'Room', 'Room_Capacity', 'Module', 'Registered_Students'])

tue_df = pd.DataFrame(index = range(10), columns=['Time', 'Date', 'Room', 'Room_Capacity', 'Module', 'Registered_Students'])

wed_df = pd.DataFrame(index = range(10), columns=['Time', 'Date', 'Room', 'Room_Capacity', 'Module', 'Registered_Students'])

thu_df = pd.DataFrame(index = range(10), columns=['Time', 'Date', 'Room', 'Room_Capacity', 'Module', 'Registered_Students'])

fri_df = pd.DataFrame(index = range(10), columns=['Time', 'Date', 'Room', 'Room_Capacity', 'Module', 'Registered_Students'])

day_tables = [mon_df, tue_df, wed_df, thu_df, fri_df]


n = 1

for table in day_tables:
    table.Time = df2[[0]].ix[1:]
    table.Module = df2[[n]].ix[1:]
    table.Registered_Students = df2[[n+1]].ix[1:]
    room = df2.columns[0]
    csroom = 'CS' + room
    table.Room= csroom
    table.Room_Capacity = df2.columns[2].split(' ')[2]
    # date. changeable
    n += 2

del n


B002_timetable = pd.concat(day_tables)

B002_timetable = B002_timetable[B002_timetable.Time.notnull()]

two_weeks = [B002_timetable, B002_timetable]

B002_timetable = pd.concat(two_weeks)

date_index = pd.date_range('2015-11-2', periods=12, freq='D')


day = 0
count = 0

while count < B002_timetable.shape[0]:
    B002_timetable.iat[count,1] = date_index[day]

    if (count + 1)% 9 == 0:
        day += 1

        if day == 5:
            day += 2

    count += 1


B002_timetable.reset_index(drop=True)