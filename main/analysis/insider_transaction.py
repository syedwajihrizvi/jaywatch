from .utils.util import percentage_change

import numpy as np


class InsiderTransactions:
    def __init__(self, name, total_holdings, last_transaction, last_transaction_date):
        self.name = name
        self.transactions = []
        self.total_holdings = total_holdings
        self.last_transaction = last_transaction
        self.last_transaction_date = last_transaction_date
        self.transaction_count = 0

    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        self.transaction_count += 1

    def analyze_transactions(self):
        self.transactions.sort(reverse=True)
        transaction_groups = {"sale": {"trans": [], "count": 0},
                              "purchase": {"trans": [], "count": 0},
                              "gift": {"trans": [], "count": 0},
                              "exer": {"trans": [], "count": 0},
                              "grant": {"trans": [], "count": 0},
                              "none": {"trans": [], "count": 0}}

        for transaction in self.transactions:
            if transaction.trans_type:
                transaction_groups[transaction.trans_type.lower()]["trans"].append(
                    transaction)
                transaction_groups[transaction.trans_type.lower()
                                   ]["count"] += 1

    def __str__(self):
        return f"{self.name} owns {self.total_holdings} and has a total of {self.transaction_count} transactions. Last transaction was {self.last_transaction}"
