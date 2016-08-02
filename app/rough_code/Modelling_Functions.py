from data_process_scripts.Linear_Regression_Creator import linear_estimate_headcount
from data_process_scripts.Logistic_Regression_Creator import binary_logistic_classifier
from data_process_scripts.Logistic_Regression_Creator import tertiary_logistic_classifier
import numpy as np
import pandas as pd


# linear functions

def prep_predictor_value(query_result):
    """Wraps a SINGLE value in a pd.DataFrame to prepare it for a StatsModels Linear Regression object

    Avg_Count_30min is the name the model was trained to predict on."""

    predictor_value = pd.DataFrame({'Avg_Count_30min': [query_result]})

    return predictor_value

def linear_prediction(predictor_value):
    """Performs a prediction on a supplied dataframe object and returns the result"""

    result = linear_estimate_headcount.predict(predictor_value)

    result = int(result)

    return result

def estimate_occupancy_number(query_result):

    predictor_value = prep_predictor_value(query_result)

    occupancy_estimate = linear_prediction(predictor_value)

    return occupancy_estimate

def prep_predictor_values(*query_results):
    """Wraps MULTIPLE values in a pd.DataFrame to prepare it for a StatsModels Linear Regression object

    Avg_Count_30min is the name the model was trained to predict on."""

    query_list = []
    for result in query_results:
        query_list.append(result)

    predictor_value = pd.DataFrame({'Avg_Count_30min': query_list})

    return predictor_value

def linear_predictions(predictor_values):
    """Performs a prediction on a supplied dataframe object and returns the result"""

    result = linear_estimate_headcount.predict(predictor_values)

    list(result)
    result = [int(x) for x in result]

    return result

def estimate_occupancy_numbers(*query_results):
    """THROWS ERROR - no dtypes ; no idea why"""

    predictor_values = prep_predictor_values(query_results)

    occupancy_estimates = linear_predictions(predictor_values)

    return occupancy_estimates


# logistic functions

def logistic_prep_values(query_result):
    """Takes one query result and prepares it for classification by logistic_classifier"""

    X = pd.DataFrame({'Avg_Count_30min': [query_result]})
    intercept = pd.DataFrame({'Intercept': np.ones(1)})
    X = pd.concat([intercept, X], axis=1)

    return X

def logistic_classifier(query_result, classifier):
    """Performs either binary or tertiary classification on supplied query. Cleans and returns result."""

    X = logistic_prep_values(query_result)

    try:
        if classifier == 'binary':
            result = binary_logistic_classifier.predict(X)
        if classifier == 'tertiary':
            result = tertiary_logistic_classifier.predict(X)
    except:
        print('Classifier must be either value "binary" or "tertiary"')
        raise(SystemExit)

    result = str(result)
    result = result.strip("[]''")

    return result