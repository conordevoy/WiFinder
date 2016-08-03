import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import cross_val_score


pd.options.mode.chained_assignment = None

# os.chdir('/home/mike/PycharmProjects/WiFinder/Data/final_csvs')

df = pd.read_csv('/home/mike/PycharmProjects/WiFinder/Data/final_csvs/ABT.csv')

ave_30 = ['Occupancy', 'Avg_Count_30min']

ave_30_3 = df[ave_30]
ave_30_2 = df[ave_30]

occupancy_three = {0.00: 'Empty', 0.25 : 'Medium', 0.50 : 'Medium', 0.75: 'High', 1.00 : 'High'}

occupancy_binary = {0.00: 'Empty', 0.25 : 'Occupied', 0.50 : 'Occupied', 0.75: 'Occupied', 1.00 : 'Occupied'}

ave_30_3['Occupancy'].replace(occupancy_three, inplace=True)

ave_30_2['Occupancy'].replace(occupancy_binary, inplace=True)





                                            # SKLearn Log Reg Prep


df.columns

# Set your dummies as necessary

date_dummies = pd.get_dummies(df.Date, prefix='Date')
module_dummies = pd.get_dummies(df.Module, prefix='Module')
room_dummies = pd.get_dummies(df.Room, prefix='Room')
hour_dummies = pd.get_dummies(df.Room, prefix='Hour')

def SKLogR(df):

    intercept = pd.DataFrame({'Intercept': np.ones(216)})
    df = pd.concat([intercept, df], axis=1)

    for i in df.columns:
        if i == 'Room':
            df = pd.concat([df, room_dummies], axis=1)
            del df['Room']

        if i == 'Date':
            df = pd.concat([df, date_dummies], axis=1)
            del df['Date']

        if i == 'Module':
            df = pd.concat([df, module_dummies], axis=1)
            del df['Module']

        if i == 'Hour':
            df = pd.concat([df, hour_dummies], axis=1)
            del df['Hour']


    X = df.ix[:, df.columns != 'Occupancy']
    Y = df.Occupancy

    for i in X.columns:
        j = i.split('_')

        if j[0] in ['Date', 'Module', 'Room', 'Hour']:
            if i == 'Room_Capacity':
                continue

            X[i] = X[i].astype('category')

    logSK = LogisticRegression().fit(X, Y)
    logSK.score(X, Y)

    scores = cross_val_score(LogisticRegression(), X, Y, scoring='accuracy', cv=12)
    print(scores.mean())

    return logSK


                                    # Logistic Model Functions


tertiary_logistic_classifier = SKLogR(ave_30_3)

binary_logistic_classifier = SKLogR(ave_30_2)