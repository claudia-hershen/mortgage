"""Mortgage Class."""
from parameters import Parameters

# Adrianc: you need to pay attention to external VS internal APIs
# protected and private methods are prefixed with _ or __ respectively
# while this is just a semantic, its honored by Python developers.

class Mortgage(object):
    """
    Mortgage - the mortgage base object.

    Params:
        payment_schedule
        amortization_period
        down_payment (optional parameter)
        parameters (Parameters)

    Operations:
        payments_per_year()
        pay_periods()

    """

    def __init__(self,
                 payment_schedule,
                 amortization_period,
                 down_payment=None):
        """
        Init Mortgage class properties when creating a new instance.

        Params:
            payment_schedule
            amortization_period
            down_payment (optional parameter)
            parameters (Parameters)
        """
        super(Mortgage, self).__init__()
        self.payment_schedule = payment_schedule
        self.amortization_period = amortization_period
        self.down_payment = down_payment
        self.parameters = Parameters()

    def payments_per_year(self):
        """Number of payments per year.

        Return:
            - monthly payment schedule -> self.parameters.months_per_year
            - biweekly payment schedule -> self.parameters.biweeks_per_year
            - weekly payment schedule -> self.parameters.weeks_per_year
        """
        
        # Adrianc: you can have a class dict member for this
        # returning Mortgage.to_payment_units['payment_schedule']
        # payment_schedule is already validated at upper layers 
        if self.payment_schedule == 'monthly':
            return self.parameters.months_per_year
        elif self.payment_schedule == 'biweekly':
            return self.parameters.biweeks_per_year
        elif self.payment_schedule == 'weekly':
            return self.parameters.weeks_per_year
        else:
            return None

    def pay_periods(self):
        """Calculate the payments period.

        e.g:
            for amortization period of 10 years and 26 payments per year
            return 10*26=260 pay periods

        Return:
            pay periods or None if payments_per_year is not available
        """
        if self.payments_per_year():
            return self.amortization_period * self.payments_per_year()
        return None
