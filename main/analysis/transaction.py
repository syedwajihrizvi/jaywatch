from .utils.util import get_year, get_month, get_day

import datetime


class Transaction:
    def __init__(self, value, shares, date, trans_type):
        self.value = value
        self.shares = shares
        self.transaction_year = get_year(date)
        self.transaction_month = get_month(date)
        self.transaction_day = get_day(date)
        self.trans_type = trans_type

    @staticmethod
    def parse_transaction_type(transaction_text):
        if "sale" in transaction_text.lower():
            return "sale"
        elif "purchase" in transaction_text.lower():
            return "purchase"
        elif "gift" in transaction_text.lower():
            return "gift"
        elif "exercise of derivative security" in transaction_text.lower():
            return "exer"
        elif "grant" in transaction_text.lower():
            return "grant"
        elif not transaction_text:
            return "none"
        else:
            return transaction_text.lower()

    def __gt__(self, other):
        d1 = datetime.datetime(self.transaction_year,
                               self.transaction_month,
                               self.transaction_day)
        d2 = datetime.datetime(other.transaction_year,
                               other.transaction_month,
                               other.transaction_day)
        return d1 > d2

    def __str__(self):
        return f"{self.trans_type}, {self.value}, {self.shares}, {self.date}"
