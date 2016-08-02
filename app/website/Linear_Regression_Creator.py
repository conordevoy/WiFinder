import os
import pandas as pd
import statsmodels.formula.api as sm
from sklearn.cross_validation import cross_val_score

os.chdir('/home/mike/PycharmProjects/WiFinder/Data/final_csvs')

df = pd.read_csv('ABT.csv')

    #
    # Deriving features:
    #
    # Occupancy count * Room Capacity: To give approximate number of students in classroom
    #


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

print(lm.summary())

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

print(lm.summary())

# replot the residuals - there is now no significant peaking and the residuals are much more stable

lm.resid.plot()


            # Create functions that will perform this regression in the working environment

linear_estimate_headcount = lm