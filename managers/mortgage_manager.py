"""MortgageManager Class."""
from __future__ import division

from models.payment_amount import PaymentAmmount
from models.mortgage_amount import MortgageAmmount
from models.parameters import Parameters

# Adrianc: you need to have an __init__ here that will contain all related objects you created in other modules
# like Parameters()
# all methods should have a well defined and documented API and not just a json blob
# e.g : maximum_mortgage(self, data)  -> maximum_mortgage(self, payment_amount, down_payment, payment_schedule, ammortization_period)
# upper layer should handle the unpacking of the data dictionary from the request.
# Alternatively you can define a new set of classes that represent a MortgageRequest whith subclasses: MaxMortgageRequest and ChangeInterestRequest
# these classes can have a validate_request() method to validate (or further validate in case of using json schema)
# the given input from the HTTP request

class MortgageManager(object):
    """Mortgage manager functions and actions."""

    def payment_per_period(self, data):
        """Get the recurring payment amount of a mortgage in $.

        Params:
            data (json) as follows:
                - asking_price - The Asking Price in $
                - payment_schedule - The Down Payment in $
                - payment_schedule - Payment schedule 'weekly'/'biweekly'/'monthly'
                - amortization_period - Amortization Period in years
        Return:
            - payment amount in $ per scheduled payment (float)
        """
        payment = PaymentAmmount(data['asking_price'],
                                 data['down_payment'],
                                 data['payment_schedule'],
                                 data['amortization_period'])
        return payment.payment_per_period

    def maximum_mortgage(self, data):
        """Get the maximum mortgage amount.

        Params:
            data (json) as follows:
                - payment_amount - payment amount per period
                - down_payment (optional) - Down Payment in $
                - payment_schedule - Payment schedule
                - amortization_period - Amortization Period
        Return:
            - Maximum mortgage in $ that can be taken (float)
        """
        if 'down_payment' in data:
            down_payment = data['down_payment']
        else:
            down_payment = None
        mortgage = MortgageAmmount(data['payment_amount'],
                                   data['payment_schedule'],
                                   data['amortization_period'],
                                   down_payment)
        return mortgage.maximum_mortgage

    def change_interest_rate(self, data):
        """Change the interest rate used by the application.

        Params:
            data (json) as follows:
                - interest_rate - The interest rate in %
        Return:
            - json indicating the old and new interest rate
        """
        parameters = Parameters()
        # Retrive current interest
        old_interets = parameters.interest_percent
        # Save new interest
        parameters.interest_percent = data['interest_rate']
        return {'old': old_interets, 'new': parameters.interest_percent}
