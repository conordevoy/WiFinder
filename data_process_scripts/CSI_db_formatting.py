import pandas as pd
import re
import data_process_scripts.functions as fn



def prep_CSI_db_files():

    df = pd.read_csv('CSI_clean.csv', header=None)

    df2 = df.ix[:, :5]

    df2 = df2.drop(df2.columns[1], axis=1)
    df2 = df2.drop(df2.columns[2], axis=1)

    b4_table = pd.DataFrame(index=range(120), columns=['Time', 'Date', 'Room', 'Occupancy'])
    b2_table = pd.DataFrame(index=range(120), columns=['Time', 'Date', 'Room', 'Occupancy'])
    b3_table = pd.DataFrame(index=range(120), columns=['Time', 'Date', 'Room', 'Occupancy'])

    room_tables = [b2_table, b3_table, b4_table]

    for room in ['B002', 'B003', 'B004']:

        n = 1
        table_count = 0
        current_date = None
        current_room = None

        day_match = re.compile(r'[A-Za-z]+day')
        date_match = re.compile(r'[1-3]?[0-9](st|rd|th|nd) November 2015')
        timeslot_match = re.compile(r'[1-2]?[0-9]\.00-([1-2]?[0-9])\.00')
        room_match = re.compile(r'{}'.format(room))

        for i in range(df2.shape[0]):


            if day_match.match(str(df2.iat[i, 0])):
                continue

            if date_match.match(str(df2.iat[i, 0])):
                current_date = str(df2.iat[i, 0])

            if room_match.match(str(df2.iat[i, 1])): # match room name
                current_room = str(df2.iat[i, 1])
                print(current_room)

            if timeslot_match.match(str(df2.iat[i, 0])):
                b2_table.iat[table_count,3] = str(df2.iat[i, 2]) # set occupancy
                b2_table.iat[table_count,0] = str(df2.iat[i, 0]) # set timeslot



            b2_table.iat[table_count,1] = current_date
            b2_table.iat[table_count,2] = room

            table_count += 1


    room_df = pd.concat(room_tables)

    room_df = room_df[room_df.Time.notnull()]

    # convert Date to datetime format
    room_df['Date'] = pd.to_datetime(room_df['Date'])

    #keep only first 2 characters in time column and remove .
    room_df['Time'] = room_df['Time'].map(lambda x: str(x)[:2])
    room_df['Time'] = room_df['Time'].map(lambda x: x.lstrip('.').rstrip('.'))

    #only keep date in Date column
    room_df['Date'] = room_df['Date'].apply(lambda x: x.date())

    #rename columns
    room_df.columns = ['Hour','Date','Room','Occupancy']

    fn.set_identifier(room_df)

    room_df.to_csv('occupancy_table.csv', index=False)
