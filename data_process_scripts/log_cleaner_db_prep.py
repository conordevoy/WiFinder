import pandas as pd
import datetime
def clean_log_files():
    df = pd.read_csv('results.csv')
    #create titles for the columns
    df.columns = ["Room", "DateTime", "Associated_count", "Authenticated_count"]
    #create 2 empty columns
    df['Building'] = ""
    df['Campus'] = ""
    #split the Room column into 3 seperate columns and getting reformatting room
    for i in range(df.shape[0]):
        value = df.iat[i, 0]
        list = value.split('> ')
        building = list[1]
        Campus = list[0]
        good_room = list[2].replace('-', '')
        df.iat[i, 0] = good_room
        df.iat[i, 4] = building
        df.iat[i, 5] = Campus
    #convert DateTime column to datetime format and only keeping the date
    #creating time column from datetime column and only keeping the time
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    df['Time'] = df['DateTime']
    df['DateTime'] = df['DateTime'].apply(lambda x: x.date())
    df['Time'] = df['Time'].apply(lambda x: x.time())
    #creating hour column and only keeping two digits while stripping leading zeros
    df["Hour"] = df["Time"]
    df["Hour"] = df["Hour"].map(lambda x: str(x)[:2])
    df['Hour'] = df['Hour'].map(lambda x: x.lstrip("0"))
    #renaming columns
    df.columns = ['Room', 'Date', 'Associated_count', 'Authenticated_count', 'Building', 'Campus', 'Time', 'Hour']
    #create an empty ID column and call function to ceate unique ID for each row
    df['ID'] = ""
    set_identifier(df)
    #save as csv
    df.to_csv('/Users/shauna/Desktop/Wifinder/WiFinder/Data/final_csvs/logdata_table.csv', index=False)