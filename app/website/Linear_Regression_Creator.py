import pandas as pd
import statsmodels.formula.api as sm
import dill as pickle
import sqlite3

db = "WiFinderDBv02.db"

conn = sqlite3.connect(db)
cur = conn.cursor()

average_logs = cur.execute("""SELECT AVG(w.Log_Count), o.Occupancy, r.Capacity
                                FROM WIFI_LOGS w JOIN OCCUPANCY o JOIN ROOM r
                                WHERE strftime('%M', w.Time) BETWEEN "15" AND "45"
                                AND  strftime('%H', w.Time) BETWEEN "09" AND "17"
                                AND  strftime('%w', w.Datetime) BETWEEN "1" AND "5"
                                AND o.ClassID = w.ClassID
                                AND r.RoomID = o.Room
                                GROUP BY w.ClassID;""") # 216 rows


df = pd.DataFrame(average_logs.fetchall())

df.columns = ['Avg_Count_30min', 'Occupancy', 'Room_Capacity']


# create new feature:
# proportion of associated count connections to room capacity

df['Room_Survey_Headcount_Estimate'] = 0.0

for row in range(df.shape[0]):
    survey = df.columns.get_loc('Occupancy')
    room_cap = df.columns.get_loc('Room_Capacity')
    headcount_col = df.columns.get_loc('Room_Survey_Headcount_Estimate')

    headcount_estimate = (df.iat[row, survey] * df.iat[row, room_cap])
    df.iat[row, headcount_col] = headcount_estimate

test_residuals = df

# plot best model - predict headcount from 30min average associated count

lm = sm.ols(formula="Room_Survey_Headcount_Estimate ~ Avg_Count_30min", data=test_residuals).fit()

# get the residual series

lm.resid

# add to df as a new column

test_residuals['residuals'] = lm.resid

# remove those values outside of 1.5 standard deviations from the mean residual
# this removes 26 observations

df_3std = test_residuals[((test_residuals.residuals - test_residuals.residuals.mean()) / test_residuals.residuals.std()).abs() < 1.5]

# visualise changes

df_3std.plot(kind='scatter', x='Avg_Count_30min', y='Occupancy');

# refit model without the possible outliers
# r^2 is significantly improved

lm = sm.ols(formula="Room_Survey_Headcount_Estimate ~ Avg_Count_30min", data=df_3std).fit()


            # Create functions that will perform this regression in the working environment

linear_estimate_headcount = lm

# write function to generate a new linear_regression function that doesn't require running the regression again.

parameters = lm.params

param_dict = parameters.to_dict()

intercept = param_dict['Intercept']
count_coefficient = param_dict['Avg_Count_30min']

with open('count_coefficient.pickle', 'wb') as handle:
    pickle.dump(count_coefficient, handle)

with open('intercept.pickle', 'wb') as handle:
    pickle.dump(intercept, handle)