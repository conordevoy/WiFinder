import os
import pandas as pd
import statsmodels.formula.api as sm


df = pd.read_csv('/home/mike/PycharmProjects/WiFinder/Data/final_csvs/ABT.csv')

df['Room_Survey_Headcount_Estimate'] = 0.0

for row in range(df.shape[0]):
    survey = df.columns.get_loc('Occupancy')
    room_cap = df.columns.get_loc('Room_Capacity')
    headcount_col = df.columns.get_loc('Room_Survey_Headcount_Estimate')

    headcount_estimate = (df.iat[row, survey] * df.iat[row, room_cap])
    df.iat[row, headcount_col] = headcount_estimate


lm = sm.ols(formula="Room_Survey_Headcount_Estimate ~ Avg_Count_30min", data=df).fit()

test_residuals = df

test_residuals['residuals'] = lm.resid

df_3std = test_residuals[((test_residuals.residuals - test_residuals.residuals.mean()) / test_residuals.residuals.std()).abs() < 1.5]

lm = sm.ols(formula="Room_Survey_Headcount_Estimate ~ Avg_Count_30min", data=df_3std).fit()

linear_estimate_headcount = lm