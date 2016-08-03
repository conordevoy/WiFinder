import dill as pickle

with open('intercept.pickle', 'rb') as handle:
    intercept = pickle.load(handle)

with open('count_coefficient.pickle', 'rb') as handle:
    count_coefficient = pickle.load(handle)

with open('tertiary_dict.pickle', 'rb') as handle:
    tertiary_break_points = pickle.load(handle)

with open('binary_dict.pickle', 'rb') as handle:
    binary_break_points = pickle.load(handle)


def linear_predictor(count):

    result = intercept + (count_coefficient * count)
    return int(result)


def binary_classifier(count):

    if count <= binary_break_points['Empty']:
        return 'Empty'
    else:
        return 'Occupied'


def tertiary_classifier(count):

    if count <= tertiary_break_points['Empty']:
        return 'Empty'

    if tertiary_break_points['Empty'] < count < tertiary_break_points['Medium']:
        return 'Medium'

    if count > tertiary_break_points['Medium']:
        return 'High'