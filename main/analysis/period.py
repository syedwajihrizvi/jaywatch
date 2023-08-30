from .utils.util import percentage_change, percentage_difference, get_year, get_month, get_day

import datetime


class Period:
    def __init__(self, end_date, period, earnings_estimate_avg,
                 eps_year_ago, revenue_estimage_avg, rev_year_ago,
                 revenue_growth, eps_trends):
        print(end_date)
        self.period_year = get_year(end_date) if end_date else None
        self.period_month = get_month(end_date) if end_date else None
        self.period_day = get_day(end_date) if end_date else None
        self.period = period
        self.earnings_estimate_avg = earnings_estimate_avg
        self.eps_year_ago = eps_year_ago
        self.revenue_estimate_avg = revenue_estimage_avg
        self.rev_year_ago = rev_year_ago
        self.revenue_growth = revenue_growth
        self.eps_trends = eps_trends

    def current_to_average_earnings_estimate(self):
        current_eps = self.eps_trends.get("current")
        if current_eps:
            percent_diff_from_earnings_estimate = percentage_difference(
                self.earnings_estimate_avg,
                current_eps
            )

    def eps_year_ago_to_current(self):
        current_eps = self.eps_trends.get("current")
        if current_eps:
            percent_diff_prev_year_eps = percentage_difference(
                current_eps,
                self.eps_year_ago
            )

    def increase_in_eps_trends(self):
        eps_change_perc = percentage_change(self.eps_trends.values())

    def __gt__(self, other):
        if not other.period_year and not other.period_month and not other.period_day:
            return True
        d1 = datetime.datetime(self.period_year,
                               self.period_month,
                               self.period_day)
        d2 = datetime.datetime(other.period_year,
                               other.period_month,
                               other.period_day)
        return d1 > d2
