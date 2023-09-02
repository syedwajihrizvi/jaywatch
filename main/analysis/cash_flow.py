class CashFlow:
    def __init__(self, investments, change_to_liabilities,
                 net_borrowings, total_cash_from_investing_activities,
                 total_cash_from_financing_activities, total_cash_from_operating_activities,
                 change_in_cash, change_to_inventory, change_to_net_income,
                 capital_expenditures, date):
        self.investments = investments
        self.change_to_liabilities = change_to_liabilities
        self.net_borrowings = net_borrowings
        self.total_cash_from_investing_activities = total_cash_from_investing_activities
        self.total_cash_from_financing_activities = total_cash_from_financing_activities
        self.total_cash_from_operating_activities = total_cash_from_operating_activities
        self.change_in_cash = change_in_cash
        self.change_to_inventory = change_to_inventory
        self.change_to_net_income = change_to_net_income
        self.capital_expenditures = capital_expenditures
        self.date = date

    def __gt__(self, other):
        return self.date > other.date
