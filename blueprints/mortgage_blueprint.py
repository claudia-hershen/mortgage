"""Mortgage Blueprint."""
from flask import abort
from flask import request
from flask import jsonify
from flask import Blueprint

from managers.mortgage_manager import MortgageManager

from validators.mortgage_validator import validate_request
from validators.mortgage_validator import validate_interest_rate_request
from validators.mortgage_validator import validate_payment_amount_request
from validators.mortgage_validator import validate_mortgage_amount_request


mortgage_blueprint = Blueprint(
    'mortgage_blueprint',
    __name__)

# Adrianc: MortgageManager can be be a singleton in the system
_mortgage_manager = MortgageManager()


@mortgage_blueprint.route('/payment-amount', methods=['GET'])
def payment_amount():
    """Get the recurring payment amount of a mortgage in $.

    Params:
        request (json) as follows:
            - asking_price - The Asking Price in $
            - down_payment - The Down Payment in $
            - payment_schedule - Payment schedule 'weekly'/'biweekly'/'monthly'
            - amortization_period - Amortization Period in years
    Return:
        - json with payment amount in $ per scheduled payment or
          json indicating request data errors or
        - for bad requests - adort with 400 error
    """
    if not validate_request(request.headers['secret_key'],
                            len(request.get_json()), [4]):
        abort(400)
    data = request.get_json()
    request_validation = validate_payment_amount_request(data)
    if request_validation['is_valid']:
        payment_per_period = _mortgage_manager.payment_per_period(data)
        return jsonify(data={'payment_per_period': payment_per_period})
    return jsonify(data={'errors': request_validation['errors']})


@mortgage_blueprint.route('/mortgage-amount', methods=['GET'])
def mortgage_amount():
    """Get the maximum mortgage amount.

    Params:
        request (json) as follows:
            - payment_amount - payment amount per period
            - down_payment (optional) - Down Payment in $
            - payment_schedule - Payment schedule
            - amortization_period - Amortization Period
    Return:
        - json with maximum mortgage in $ that can be taken
        - json indicating request data errors
        - for bad requests - adort with 400 error
    """
    if not validate_request(request.headers['secret_key'],
                            len(request.get_json()), [3, 4]):
        abort(400)
    data = request.get_json()
    request_validation = validate_mortgage_amount_request(data)
    if request_validation['is_valid']:
        maximum_mortgage = _mortgage_manager.maximum_mortgage(data)
        return jsonify(data={'maximum_mortgage': maximum_mortgage})
    return jsonify(data={'errors': request_validation['errors']})


@mortgage_blueprint.route('/interest-rate', methods=['PATCH'])
def interest_rate():
    """Change the interest rate used by the application.

    Params:
        request (json) as follows:
            - interest_rate - The interest rate
    Return:
        - json indicating the old and new interest rate
        - json indicating request data errors
        - for bad requests - adort with 400 error
    """
    if not validate_request(request.headers['secret_key'],
                            len(request.get_json()), [1]):
        abort(400)
    data = request.get_json()
    request_validation = validate_interest_rate_request(data)
    if request_validation['is_valid']:
        interest_rate = _mortgage_manager.change_interest_rate(data)
        return jsonify(data={'old_interest_rate': interest_rate['old'],
                             'new_interest_rate': interest_rate['new']})
    return jsonify(data={'errors': request_validation['errors']})
