import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import cross_val_score
from numpy import ones
from pandas import DataFrame, concat
import dill as pickle
import sqlite3

pd.options.mode.chained_assignment = None

db = "WiFinderDBv02.db"

conn = sqlite3.connect(db)
cur = conn.cursor()

average_logs = cur.execute("""SELECT AVG(w.Log_Count), o.Occupancy
                                FROM WIFI_LOGS w JOIN OCCUPANCY o JOIN ROOM r
                                WHERE strftime('%M', w.Time) BETWEEN "15" AND "45"
                                AND  strftime('%H', w.Time) BETWEEN "09" AND "17"
                                AND  strftime('%w', w.Datetime) BETWEEN "1" AND "5"
                                AND o.ClassID = w.ClassID
                                GROUP BY w.ClassID;""") # 216 rows


df = pd.DataFrame(average_logs.fetchall())

df.columns = ['Avg_Count_30min', 'Occupancy']

ave_30 = ['Occupancy', 'Avg_Count_30min']

ave_30_3 = df[ave_30]
ave_30_2 = df[ave_30]

occupancy_three = {0.00: 'Empty', 0.25 : 'Medium', 0.50 : 'Medium', 0.75: 'High', 1.00 : 'High'}

occupancy_binary = {0.00: 'Empty', 0.25 : 'Occupied', 0.50 : 'Occupied', 0.75: 'Occupied', 1.00 : 'Occupied'}

ave_30_3['Occupancy'].replace(occupancy_three, inplace=True)

ave_30_2['Occupancy'].replace(occupancy_binary, inplace=True)





                                            # SKLearn Log Reg Prep

def SKLogR(df):

    intercept = pd.DataFrame({'Intercept': ones(216)}) # this will need to be updated; ONLY HOLDS FOR CURRENT DATABASE
    df = pd.concat([intercept, df], axis=1)

    X = df.ix[:, df.columns != 'Occupancy']
    Y = df.Occupancy

    logSK = LogisticRegression().fit(X, Y)

    scores = cross_val_score(LogisticRegression(), X, Y, scoring='accuracy', cv=12)
    # print(scores.mean())

    return logSK


                                    # Logistic Model Functions


tertiary_logistic_classifier = SKLogR(ave_30_3)

binary_logistic_classifier = SKLogR(ave_30_2)

def logistic_prep_values(query_result):
    """Takes one query result and prepares it for classification by logistic_classifier"""

    X = DataFrame({'Avg_Count_30min': [query_result]})
    intercept = DataFrame({'Intercept': ones(1)})
    X = concat([intercept, X], axis=1)

    return X

def logistic_classifier(query_result, classifier):
    """Performs either binary or tertiary classification on supplied query. Cleans and returns result."""

    if query_result is None:
        query_result = -65535
    X = logistic_prep_values(query_result)

    if classifier == 'binary':
        result = binary_logistic_classifier.predict(X)
    elif classifier == 'tertiary':
        result = tertiary_logistic_classifier.predict(X)
    else:
        print('Classifier = ', classifier, '. Invalid input')

    result = str(result)
    result = result.strip("[]''")

    return result


def find_break_point_tertiary():
    """Finds where a classifier switches value for a given int. Ranges 1-1000000"""

    break_points = {}
    class_list = ['Empty', 'Medium']
    list_position = 0

    for i in range(1000000):

        predicted_value = logistic_classifier(i, 'tertiary')
        if predicted_value == class_list[list_position]:
            continue

        else:
            break_points[class_list[list_position]] = (i - 1)
            if predicted_value == 'High':
                break
            list_position += 1

    return break_points


def find_break_point_binary():
    """Finds where a classifier switches value for a given int. Ranges 1-1000000"""

    break_points = {}
    empty = 'Empty'

    for i in range(1000000):

        predicted_value = logistic_classifier(i, 'binary')

        if predicted_value == empty:
            continue
        else:
            break_points[empty] = i
            break

    return break_points

tertiary_break_points = find_break_point_tertiary()

binary_break_points = find_break_point_binary()

with open('binary_dict.pickle', 'wb') as handle:
    pickle.dump(binary_break_points, handle)

with open('tertiary_dict.pickle', 'wb') as handle:
    pickle.dump(tertiary_break_points, handle)