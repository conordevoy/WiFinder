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


                                 #         Linear Regressions 1
                                 #
                                 #          Predict: Occupancy
                                 #
                                 #
                                 #              Features:
                                 #
                                 #      Average Count over 60 minutes
                                 #      Average Count over 30 minutes
                                 # Adjusted Average Count over 60 minutes
                                 # Adjusted Average Count over 30 minutes


lm = sm.ols(formula="Occupancy ~ Avg_Count_60min", data=df).fit()

print(lm.summary())

lm = sm.ols(formula="Occupancy ~ Avg_Count_30min", data=df).fit()

print(lm.summary())

lm = sm.ols(formula="Occupancy ~ Avg_Adj_Count_60min", data=df).fit()

print(lm.summary())

lm = sm.ols(formula="Occupancy ~ Avg_Adj_Count_30min", data=df).fit()

print(lm.summary())

                            #
                            #              Linear Regressions 2
                            #
                            # Adjusted30min is the highest scoring on Occupancy.
                            #
                            #               Predict: Occupancy
                            #
                            #                   Features:
                            #
                            #           Average Count over 60 minutes
                            #           Average Count over 30 minutes
                            #      Adjusted Average Count over 60 minutes
                            #      Adjusted Average Count over 30 minutes


lm = sm.ols(formula="Room_Survey_Headcount_Estimate ~ Avg_Count_60min", data=df).fit()

print(lm.summary())

lm = sm.ols(formula="Room_Survey_Headcount_Estimate ~ Avg_Count_30min", data=df).fit()

print(lm.summary())

lm = sm.ols(formula="Room_Survey_Headcount_Estimate ~ Avg_Adj_Count_60min", data=df).fit()

print(lm.summary())

lm = sm.ols(formula="Room_Survey_Headcount_Estimate ~ Avg_Adj_Count_30min", data=df).fit()

print(lm.summary())


                       #                       Linear Results 3:
                       #
                       #  Adjusted30min is the highest scoring on occupancy.
                       #  Avg30min is the highest scoring on headcount_estimate.
                       #
                       # Next, we attempt normalisation to deal with outliers.
                       # We repeat the previous two winning regressions from each step.


df_norm = df

df_norm['Norm_Avg_Adj_Count_30min'] = df_norm['Avg_Adj_Count_30min']
df_norm['Norm_Avg_Count_30min'] = df_norm['Avg_Count_30min']

cols_to_norm = ['Norm_Avg_Count_30min', 'Norm_Avg_Adj_Count_30min']
df[cols_to_norm] = df[cols_to_norm].apply(lambda x: (x - x.min()) / (x.max() - x.min()))



# OLS with normalised adjusted 30minute count, predicting occupancy

lm = sm.ols(formula="Occupancy ~ Norm_Avg_Adj_Count_30min", data=df).fit()

print(lm.summary())

# OLS with normalised 30minute count, predicting headcount

lm = sm.ols(formula="Room_Survey_Headcount_Estimate ~ Norm_Avg_Count_30min", data=df).fit()

print(lm.summary())

test_residuals = lm.resid

# plot residuals

lm.resid.plot()

# residuals are significantly peaked, especially at the higher end of the occupancy scale


# test fitting residual series to model and then removing >3 sd instances and replotting residuals.


test_residuals = df

# plot best model - predict headcount from 30min average associated count

lm = sm.ols(formula="Room_Survey_Headcount_Estimate ~ Norm_Avg_Count_30min", data=test_residuals).fit()

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