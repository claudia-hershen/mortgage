"""MortgageAmmount Class."""
from mortgage import Mortgage


class MortgageAmmount(Mortgage):
    """MortgageAmmount - Inherit from Mortgage."""

    def __init__(self,
                 payment_amount,
                 payment_schedule,
                 amortization_period,
                 down_payment=None):
        """
        Init PaymentAmmount class properties when creating a new instance.

        Params:
            payment_amount
            down_payment
            payment_schedule
            amortization_period
        """
        super(MortgageAmmount, self).__init__(
            payment_schedule, amortization_period, down_payment)
        self.payment_amount = payment_amount
        self.maximum_mortgage = self._maximum_mortgage()

    def _maximum_mortgage(self):
        """Calculate the maximum mortgage amount.

        Return:
            Maximum mortgage in $ that can be taken (float)
        """
        if self.down_payment:
            return self._maximum_mortgage_with_down_payment()
        else:
            return self._maximum_mortgage_no_down_payment()

    def _maximum_mortgage_no_down_payment(self):
        """Calculate maximum mortgage with NO down payment.

        Return:
            Maximum mortgage in $ that can be taken (float)
        """
        interest_amount = self._interest_amount()
        return round(self.payment_amount * interest_amount, 2)

    def _maximum_mortgage_with_down_payment(self):
        """Calculate maximum mortgage with down payment.

        If down payment is included its value should be added to
        the maximum mortgage returned
        Return:
            Maximum mortgage in $ that can be taken (float)
        """
        mortgage_without_down_payment = self._maximum_mortgage_no_down_payment()
        return round(self.down_payment + mortgage_without_down_payment, 2)

    def _interest_amount(self):
        """Calculate interest multiplier.

        Return:
            insurance amount as a float value
        """
        interest = (
            self.parameters.interest_percent / self.payments_per_year() / 100)
        multiplier = pow(1 + interest, self.pay_periods())
        return (multiplier - 1) / (interest * multiplier)
