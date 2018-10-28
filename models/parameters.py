"""Parameters Class."""

INTEREST_FILE_PATH = 'interest.txt'


class Parameters(object):
    """
    Parameters - Class with parameters used by the app.

    Params:
        recipes (RecipeVersion)
    """

    def __init__(self):
        """
        Init Parameters class properties when creating a new instance.

        Params:
            _interest_percent
            insurances_costs
            weeks_per_year
            biweeks_per_year
            months_per_year
        """
        super(Parameters, self).__init__()
        # get default interest rate from file
        interest_file = open(INTEREST_FILE_PATH)
        default_interest = interest_file.read()
        interest_file.close()

        self._interest_percent = float(default_interest)
        self.insurances_costs = [
            {'down_payment_percent': 9.99, 'inaurance_cost_percent': 3.15},
            {'down_payment_percent': 14.99, 'inaurance_cost_percent': 2.4},
            {'down_payment_percent': 19.99, 'inaurance_cost_percent': 1.8}]
        self.weeks_per_year = 52
        self.biweeks_per_year = self.weeks_per_year / 2
        self.months_per_year = 12

    @property
    def interest_percent(self):
        """__interest_percent property gettet.

        Return:
            _interest_percent - the interest rate
        """
        return self._interest_percent

    @interest_percent.setter
    def interest_percent(self, value):
        """__interest_percent property setter.

        Changes __interest_percent value and saves it to file.
        Params:
            value - the new value of the ineterest in %
        """
        if (value != self._interest_percent):
            interest_file = open(INTEREST_FILE_PATH, 'w')
            interest_file.write(str(value))
            interest_file.close()
            self._interest_percent = value
