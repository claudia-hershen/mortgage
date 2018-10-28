"""PaymentAmmount Class."""
from mortgage import Mortgage


class PaymentAmmount(Mortgage):
    """PaymentAmmount - Inherit from Mortgage."""

    def __init__(self,
                 asking_price,
                 down_payment,
                 payment_schedule,
                 amortization_period):
        """
        Init PaymentAmmount class properties when creating a new instance.

        Params:
            asking_price
            down_payment
            payment_schedule
            amortization_period
        """
        super(PaymentAmmount, self).__init__(
            payment_schedule, amortization_period, down_payment)
        self.asking_price = asking_price
        self.payment_per_period = self._payment_per_period()

    def _payment_per_period(self):
        """Calculate the recurring payment amount.

        Return:
            - payment amount in $ per scheduled payment period (float)
        """
        loan_principal = self._loan_principal()
        insurance_cost = self._insurance_cost(loan_principal)
        new_loan_principal = loan_principal + insurance_cost
        return round(new_loan_principal * self._interest_amount(), 2)

    def _loan_principal(self):
        """Calculate the loan principal.

        Return:
            loan principal calculation result
        """
        return self.asking_price - self.down_payment

    def _insurance_cost(self, loan_principal):
        """Calculate insurance cost.

        Params:
            loan_principal
        Return:
            insurance cost calculation result or zero
        """
        down_payment_percent = self.down_payment / self.asking_price * 100
        for insurance in self.parameters.insurances_costs:
            if down_payment_percent <= insurance['down_payment_percent']:
                return (
                    loan_principal * insurance['inaurance_cost_percent'] / 100)
        return 0

    def _interest_amount(self):
        """Calculate interest ammount (c(1 + c)^n]/[(1 + c)^n - 1).

        Return:
            interest amount as a float value
        """
        interest = (
            self.parameters.interest_percent / self.payments_per_year() / 100)
        multiplier = pow(1 + interest, self.pay_periods())
        return (interest * multiplier) / (multiplier - 1)
