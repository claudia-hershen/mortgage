"""A wrapper for Mortgage Calculatot app.

This is a way to run the restful API from the browser.
Run as follows:
    - GET /payment-amount:
        - /run/payment-amount in browser
        - change json_obj param as required
    - GET /mortgage-amount:
        - with down payment - /run/mortgage-amount-full in browser
        - without down payment - /run/mortgage-amount-partial in browser
        - change json_obj param as required
    - PATCH /interest-rate:
        - /run/interest-rate in browser
        - change json_obj param as required
Each call will make a request object and send it to mortgage_blueprint.
"""
import json
import requests

from flask import jsonify
from flask import Response
from flask import Blueprint

run_wrapper_blueprint = Blueprint(
    'run_wrapper_blueprint',
    __name__,
    url_prefix='/run')

BASE_URL = 'http://127.0.0.1:5000'
SECRET_KEY = 'any secret string'
ERROR_MSG = "Sorry, couldn't perform request because:"


@run_wrapper_blueprint.route('/payment-amount')
def run_payment_amount():
    """Create and send requests to mortgage_blueprint.payment_amount.

    Return:
        - response json object in case of success
        - error message in case of failure
    """
    path = 'payment-amount'
    request_url = "{}/{}".format(BASE_URL, path)
    json_obj = {'asking_price': 1000000,
                'down_payment': 200000,
                'payment_schedule': 'biweekly',
                'amortization_period': 15}
    response = requests.get(
        request_url,
        data=json.dumps(json_obj),
        headers={'Content-Type': 'application/json',
                 'secret_key': SECRET_KEY})
    if response.status_code == 200:
        return jsonify(response.json())
    return Response("{} {}".format(ERROR_MSG, response.text))


@run_wrapper_blueprint.route('/mortgage-amount-full')
def run_mortgage_amount_full():
    """Create and send requests to mortgage_blueprint.mortgage_amount.

    Return:
        - response json object in case of success
        - error message in case of failure
    """
    path = 'mortgage-amount'
    request_url = "{}/{}".format(BASE_URL, path)
    json_obj = {'payment_amount': 2538,
                'down_payment': 200000,
                'payment_schedule': 'biweekly',
                'amortization_period': 15}
    response = requests.get(
        request_url,
        data=json.dumps(json_obj),
        headers={'Content-Type': 'application/json',
                 'secret_key': SECRET_KEY})
    if response.status_code == 200:
        return jsonify(response.json())
    return Response("{} {}".format(ERROR_MSG, response.text))


@run_wrapper_blueprint.route('/mortgage-amount-partial')
def run_mortgage_amount_partial():
    """Create and send requests to mortgage_blueprint.mortgage_amount.

    Return:
        - response json object in case of success
        - error message in case of failure
    """
    path = 'mortgage-amount'
    request_url = "{}/{}".format(BASE_URL, path)
    json_obj = {'payment_amount': 2538,
                'payment_schedule': 'monthly',
                'amortization_period': 15}
    response = requests.get(
        request_url,
        data=json.dumps(json_obj),
        headers={'Content-Type': 'application/json',
                 'secret_key': SECRET_KEY})
    if response.status_code == 200:
        return jsonify(response.json())
    return Response("{} {}".format(ERROR_MSG, response.text))


@run_wrapper_blueprint.route('/interest-rate')
def run_interest_rate():
    """Create and send requests to mortgage_blueprint.interest_rate.

    Return:
        - response json object in case of success
        - error message in case of failure
    """
    path = 'interest-rate'
    request_url = "{}/{}".format(BASE_URL, path)
    json_obj = {'interest_rate': 2.5}
    response = requests.patch(
        request_url,
        data=json.dumps(json_obj),
        headers={'Content-Type': 'application/json',
                 'secret_key': SECRET_KEY})
    if response.status_code == 200:
        return jsonify(response.json())
    return Response("{} {}".format(ERROR_MSG, response.text))
