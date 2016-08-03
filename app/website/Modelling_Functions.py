from data_process_scripts.Linear_Regression_Creator import linear_estimate_headcount
from data_process_scripts.Logistic_Regression_Creator import binary_logistic_classifier
from data_process_scripts.Logistic_Regression_Creator import tertiary_logistic_classifier
from numpy import ones
from pandas import DataFrame, concat


# linear functions

def prep_predictor_value(query_result):
    """Wraps a SINGLE value in a pd.DataFrame to prepare it for a StatsModels Linear Regression object

    Avg_Count_30min is the name the model was trained to predict on."""

    predictor_value = DataFrame({'Avg_Count_30min': [query_result]})

    return predictor_value

def linear_prediction(predictor_value):
    """Performs a prediction on a supplied dataframe object and returns the result"""

    result = linear_estimate_headcount.predict(predictor_value)

    result = int(result)

    return result

def test(count):

    count_in_dataframe = prep_predictor_value(count)
    predicted_value = linear_prediction(count_in_dataframe)

    return predicted_value

# def prep_predictor_values(*query_results):
#     """Wraps MULTIPLE values in a pd.DataFrame to prepare it for a StatsModels Linear Regression object
#
#     Avg_Count_30min is the name the model was trained to predict on."""
#
#     query_list = []
#     for result in query_results:
#         query_list.append(result)
#
#     predictor_value = DataFrame({'Avg_Count_30min': query_list})
#
#     return predictor_value
#
# def linear_predictions(predictor_values):
#     """Performs a prediction on a supplied dataframe object and returns the result"""
#
#     result = linear_estimate_headcount.predict(predictor_values)
#
#     list(result)
#     result = [int(x) for x in result]
#
#     return result
#
# def estimate_occupancy_numbers(*query_results):
#     """THROWS ERROR - no dtypes ; no idea why"""
#
#     predictor_values = prep_predictor_values(query_results)
#
#     occupancy_estimates = linear_predictions(predictor_values)
#
#     return occupancy_estimates


# logistic functions

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

    # try:
    if classifier == 'binary':
        result = binary_logistic_classifier.predict(X)
    elif classifier == 'tertiary':
        result = tertiary_logistic_classifier.predict(X)
    else:
        print('Classifier = ', classifier, '. Invalid input')
    # except:
    #     print('Classifier must be either value "binary" or "tertiary"')
    #     raise(SystemExit)

    result = str(result)
    result = result.strip("[]''")

    return result

def hardwire_linear(number):
    '''hardwires parameters for linear regression'''

    if number is None:
        number = -65535

    headcount = 0.710338 + (.933441 * number)

    return int(headcount)

print(hardwire_linear(100))