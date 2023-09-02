class BalanceSheet:
    def __init__(self, intangible_assets, capital_surplus,
                 total_liab, other_current_liab, end_date,
                 other_current_assets, retained_earnings,
                 treasury_stock, other_assets, cash,
                 total_current_liabilities, short_long_term_debt,
                 total_current_assets, short_term_investments,
                 long_term_debt):
        self.intangible_assets = intangible_assets
        self.total_liab = total_liab
        self.capital_surplus = capital_surplus
        self.other_current_liab = other_current_liab
        self.end_date = end_date
        self.other_current_assets = other_current_assets
        self.retained_earnings = retained_earnings
        self.treasury_stock = treasury_stock
        self.other_assets = other_assets
        self.cash = cash
        self.total_current_liabilities = total_current_liabilities
        self.short_long_term_debt = short_long_term_debt
        self.total_current_assets = total_current_assets
        self.short_term_investments = short_term_investments
        self.long_term_debt = long_term_debt

    def __gt__(self, other):
        return self.end_date > other.end_date
