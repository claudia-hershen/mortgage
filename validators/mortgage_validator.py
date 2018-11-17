"""."""

# Adrianc: these validator utilities are not needed IMO.
from utility.validator_utility import is_number
from utility.validator_utility import number_bigger_than
from utility.validator_utility import number_smaller_than
from utility.validator_utility import is_negative_number

# Adrianc: the entire validation process can be done against a json schema https://json-schema.org/
# you can create a schema per request and avoid the hardcoded logic here.
# the following comments will regard to the code
# (i.e assuming you go with non schema based validation, what can be improved)


# Adrianc: the below code can be composed into a class

# Adrianc: The entire error handing thourghout the code should be exception based which should be in a dedicate module
# e.g exceptions/param_validation_errors.py which will contain exception derrived from exceptions/base.py base exception class
# A validation shall emit an exception on the first error it encounters.

# Adrianc: Those can be class members as they are fixed for all instances
SECRET_KEY = 'any secret string'
EXPENSIVE_HOUSE_PRICE = 1000000
MEDIUM_HOUSE_PRICE = 500000
EXPENSIVE_HOUSE_MIN_DOWN_PAYMENT_PERCENT = 20
MEDIUM_HOUSE_MIN_DOWN_PAYMENT_PERCENT_LOW = 5
MEDIUM_HOUSE_MIN_DOWN_PAYMENT_PERCENT_HIGH = 10


# Adrianc: what is it that you are trying to validate here here ?
def validate_request(request_key, request_length, real_length):
    """Validate if the request is formed properly.

    A request is allowed to proceed if it:
        - Has the right secret key
        - Has the right amount of parameters
    Params:
        - request_key - The key of the request
        - request_length - The ammount of parameters that the request have
        - real_length - The real value that request_length should be
    Return:
        - True / False
    """
    return (request_key == SECRET_KEY and request_length in real_length)


def validate_interest_rate_request(data):
    """Validate interest rate data.

    Params:
        data (json) with the following fields:
            interest_rate - Interest rate should be a number between 0 and 100.
    Return:
        json object as follows:
            is_valid - True if the data is valid, otherwise False
            errors - json objects with errors details
    """
    is_valid = True
    errors = {}
    # Adrianc: 'interest_rate' is fixed key, should be a Const defined as a class memeber or a different ConstsClass
    # same goes for the rest of the keys used in this code.
    # Also why not fail on the first error ? the params constraint should be documented in the REST API documentation
    # User is in charge of READING this documentation before attempttion to use the API.
    errors['interest_rate'] = []
    if 'interest_rate' in data:
        interest = data['interest_rate']
        if is_number(interest):
            if (number_smaller_than(interest, 0) or
               number_bigger_than(interest, 100)):
                is_valid = False
                errors['interest_rate'].append(
                    'Interest rate must be in range of: 0 - 100')
        else:
            is_valid = False
            errors['interest_rate'].append('Interest rate must be a number')
    else:
        is_valid = False
        errors['interest_rate'].append('Interest rate is missing')
    return {'is_valid': is_valid, 'errors': errors}


def validate_mortgage_amount_request(data):
    """Validate mortgage amount data.

    Params:
        data (json) with the following fields:
            payment_amount - Payment amount in $
            down_payment - Down payment in $ (optional)
            payment_schedule - Payment schedule 'weekly'/'biweekly'/'monthly'
            amortization_period - Amortization period in years
    Return:
        json object as follows:
            is_valid - True if the data is valid, otherwise False
            errors - json objects with errors details
    """
    is_valid = True
    errors = {}
    errors['payment_amount'] = []
    errors['down_payment'] = []
    errors['payment_schedule'] = []
    errors['amortization_period'] = []

    # Validate payment_amount
    if 'payment_amount' in data:
        payment_amount = data['payment_amount']
        if not is_number(payment_amount) or is_negative_number(payment_amount):
            is_valid = False
            errors['payment_amount'].append(
                'Payment amount must be a positive numbe')
    else:
        is_valid = False
        errors['payment_amount'].append('Payment amount is missing')

    # Validate down_payment (optional value)
    if 'down_payment' in data:
        down_payment = data['down_payment']
        if not is_number(down_payment) or is_negative_number(down_payment):
            is_valid = False
            errors['down_payment'].append(
                'Down payment amount must be a positive numbe')

    # Validate payment_schedule
    payment_schedule_invalid = validate_payment_schedule(data)
    if payment_schedule_invalid:
        is_valid = False
        errors['payment_schedule'].append(
            payment_schedule_invalid['payment_schedule'])

    # Validate amortization_period
    amortization_period_invalid = validate_amortization_period(data)
    if amortization_period_invalid:
        is_valid = False
        errors['amortization_period'].append(
            amortization_period_invalid['amortization_period'])
    return {'is_valid': is_valid, 'errors': errors}


def validate_payment_amount_request(data):
    """Validate payment amount data.

    Params:
        data (json) with the following fields:
            asking_price - Asking price in $
            down_payment - Down payment in $
            payment_schedule - Payment schedule 'weekly'/'biweekly'/'monthly'
            amortization_period - Amortization period in years
    Return:
        json object with the following fields:
            is_valid - True if the data is valid, otherwise False
            errors - json objects with errors details
    """
    is_valid = True
    errors = {}
    errors['asking_price'] = []
    errors['down_payment'] = []
    errors['payment_schedule'] = []
    errors['amortization_period'] = []

    # Validate asking_price
    if 'asking_price' in data:
        asking_price = data['asking_price']
        if not is_number(asking_price) or is_negative_number(asking_price):
            is_valid = False
            errors['asking_price'].append(
                'Asking price must be a positive number')
    else:
        is_valid = False
        errors['asking_price'].append('Asking price is missing')

    # Validate down_payment
    if 'down_payment' in data:
        down_payment = data['down_payment']
        if not is_number(down_payment) or is_negative_number(down_payment):
            is_valid = False
            errors['down_payment'].append('Down payment must be a positive number')
    else:
        is_valid = False
        errors['down_payment'].append('Down payment is missing')

    # If no errors so far
    if is_valid:
        down_payment_invalid = validate_down_payment_and_asking_price(
            data['down_payment'], data['asking_price'])
        if down_payment_invalid:
            is_valid = False
            errors['down_payment'].append(down_payment_invalid['down_payment'])

    # Validate payment_schedule
    payment_schedule_invalid = validate_payment_schedule(data)
    if payment_schedule_invalid:
        is_valid = False
        errors['payment_schedule'].append(
            payment_schedule_invalid['payment_schedule'])

    # Validate amortization_period
    amortization_period_invalid = validate_amortization_period(data)
    if amortization_period_invalid:
        is_valid = False
        errors['amortization_period'].append(
            amortization_period_invalid['amortization_period'])
    return {'is_valid': is_valid, 'errors': errors}


def validate_down_payment_and_asking_price(down_payment, asking_price):
    """Down payment must be as specified below.

    At least 5% of first $500k plus 10% of any amount above $500k
    e.g: down payment will be $50k on a $750k mortgage)
    Params:
        down_payment - Down payment in $
        asking_price - Asking price in $
    Return:
        If not valid - json with errors
        If valid - None
    """
    if number_bigger_than(down_payment, asking_price):
        error = 'Asking price must be bigger than the down payment'
        return {'down_payment': error}
    if number_bigger_than(asking_price, EXPENSIVE_HOUSE_PRICE):
        expensive_house_down_payment = (
            asking_price * EXPENSIVE_HOUSE_MIN_DOWN_PAYMENT_PERCENT / 100)
        if number_smaller_than(down_payment, expensive_house_down_payment):
            error = 'For a house price above $1 million down payment must be at least {}%'.format(
                    EXPENSIVE_HOUSE_MIN_DOWN_PAYMENT_PERCENT)
            return {'down_payment': error}
    elif number_bigger_than(asking_price, MEDIUM_HOUSE_PRICE):
        medium_house_down_payment = (
            MEDIUM_HOUSE_PRICE * MEDIUM_HOUSE_MIN_DOWN_PAYMENT_PERCENT_LOW / 100 +
            (asking_price - MEDIUM_HOUSE_PRICE) * MEDIUM_HOUSE_MIN_DOWN_PAYMENT_PERCENT_HIGH / 100)
        if number_smaller_than(down_payment, medium_house_down_payment):
            error = 'For a house price above $500K down payment must be at least {}% of first $500K plus {}% of any amount above $500K'.format(
                MEDIUM_HOUSE_MIN_DOWN_PAYMENT_PERCENT_LOW,
                MEDIUM_HOUSE_MIN_DOWN_PAYMENT_PERCENT_HIGH)
            return {'down_payment': error}
    else:
        cheap_house_down_payment = (
            asking_price * MEDIUM_HOUSE_MIN_DOWN_PAYMENT_PERCENT_LOW / 100)
        if number_smaller_than(down_payment, cheap_house_down_payment):
            error = 'For a house price below $500K down payment must be at least {}%'.format(
                    MEDIUM_HOUSE_MIN_DOWN_PAYMENT_PERCENT_LOW)
            return {'down_payment': error}
    return None


def validate_payment_schedule(data):
    """Payment schedule should be one of: weekly, biweekly or monthly.

    Params:
        A json with data
    Return:
        If not valid - json with error
        If valid - None
    """
    if 'payment_schedule' in data:
        payment_schedule = data['payment_schedule']
        if not check_payment_schedule(payment_schedule):
            return {'payment_schedule': 'Payment schedule is incorrect'}
    else:
        return {'payment_schedule': 'Payment schedule is missing'}
    return None


def validate_amortization_period(data):
    """Amortization period should be: min 5 years, max 25 years.

    Params:
        A json with data
    Return:
        If not valid - json with errors
        If valid - None
    """
    if 'amortization_period' in data:
        amortization_period = data['amortization_period']
        if is_number(amortization_period):
            if (number_smaller_than(amortization_period, 5) or
               number_bigger_than(amortization_period, 25)):
                error = 'Amortization period must be in range of: 5-25 years'
                return {'amortization_period': error}
        else:
            error = 'Amortization period must be a number'
            return {'amortization_period': error}
    else:
        error = 'Amortization period is missing'
        return {'amortization_period': error}
    return None


def check_payment_schedule(test_schedule):
    """Check if test_schedule is correct.

    A correct test_schedule must be one of: 'weekly', 'biweekly', 'monthly'

    Params:
        test_schedule
    Return:
        True or False
    """
    schedule = ['weekly', 'biweekly', 'monthly']
    return test_schedule in schedule
