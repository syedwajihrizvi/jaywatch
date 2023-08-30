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
        self.transactions.sort()
        transaction_groups = {"sale": {"trans": [], "avg": [], "delta": []},
                              "purchase": {"trans": [], "avg": [], "delta": []},
                              "gift": {"trans": [], "avg": [], "delta": []},
                              "exer": {"trans": [], "avg": [], "delta": []},
                              "grant": {"trans": [], "avg": [], "delta": []},
                              "none": {"trans": [], "avg": [], "delta": []}}

        for transaction in self.transactions:
            if transaction.trans_type:
                transaction_groups[transaction.trans_type.lower()]["trans"].append(
                    transaction)

        for groups in transaction_groups.values():
            groups["delta"] = percentage_change(
                [trans.shares for trans in groups["trans"]])
            groups["avg"] = np.average(
                [trans.shares for trans in groups["trans"]])

        # Sort the latest transactions by which ones most recent
        most_recent_trans_of_each_type = []
        for trans_data in transaction_groups.values():
            recent_trans = trans_data.get("trans")
            if recent_trans:
                recent_trans = recent_trans[0]
            else:
                recent_trans = None
            most_recent_trans_of_each_type.append(trans_data.get("trans"))

        most_recent_trans_of_each_type = [
            trans[0] for trans in most_recent_trans_of_each_type if trans]
        most_recent_trans_of_each_type.sort()
        most_recent_trans_of_each_type = [
            trans.trans_type for trans in most_recent_trans_of_each_type]
        if self.last_transaction in most_recent_trans_of_each_type:
            most_recent_trans_of_each_type.remove(self.last_transaction)
            most_recent_trans_of_each_type.insert(0, self.last_transaction)

        self.trans_type_recency_rankings = most_recent_trans_of_each_type
        for trans_type in most_recent_trans_of_each_type:
            data = transaction_groups[trans_type]
            first_type = data["trans"][0]
            greater_shares_than_avg = first_type.shares > data["avg"]
            data["last_one_more_than_avg"] = greater_shares_than_avg
            if self.total_holdings:
                percent_of_total = (first_type.shares/self.total_holdings)*100
                self.last_one_percent_of_total = percent_of_total

    def __str__(self):
        return f"{self.name} owns {self.total_holdings} and has a total of {self.transaction_count} transactions. Last transaction was {self.last_transaction}"
