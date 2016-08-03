def hardwire_linear(number):
    '''hardwires parameters for linear regression'''

    if number is None:
        number = -65535

    headcount = 0.710338 + (.933441 * number)

    return int(headcount)

def hardwire_binary(number):
    '''hardwires parameters for linear regression'''

    if number is None:
        number = -65535

    if number >= 10:
        value = 'Occupied'

    else:
        value = 'Empty'

    return value

def hardwire_tertiary(number):
    '''hardwires parameters for linear regression'''

    if number is None:
        number = -65535

    if number > 1100:
        value = 'High'

    elif 12 <= number <= 1100:
        value = 'Medium'

    else:
        value = 'Empty'

    return value
