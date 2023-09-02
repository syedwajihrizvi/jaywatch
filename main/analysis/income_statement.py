class IncomeStatement:
    def __init__(self, r_and_d, income_before_tax,
                 net_income, gross_profit, operating_income,
                 other_operating_expenses, total_revenue,
                 end_date):
        self.r_and_d = r_and_d
        self.income_before_tax = income_before_tax
        self.net_income = net_income
        self.gross_profit = gross_profit
        self.operating_income = operating_income
        self.other_operating_expenses = other_operating_expenses
        self.total_revenue = total_revenue
        self.end_date = end_date

    def __gt__(self, other):
        return self.end_date > other.end_date
