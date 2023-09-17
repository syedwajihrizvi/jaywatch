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

    def year_ago_rev_to_estimate(self):
        change_in_two_year_rev = percentage_difference(
            self.rev_year_ago, self.revenue_estimate_avg)

    def eps_trend_change(self):
        trend_vals = list(self.eps_trends.values())
        trend_vals = [val for val in trend_vals if not isinstance(val, dict)]
        if trend_vals:
            change_in_eps_by_days = percentage_change(
                list(self.eps_trends.values()))

    def year_ago_eps_to_now(self):
        if self.eps_trends.get("current") and self.eps_year_ago:
            eps_year_diff = percentage_difference(
                self.eps_year_ago, self.eps_trends.get("current"))

    def year_ago_eps_to_estimate(self):
        if self.eps_year_ago and self.earnings_estimate_avg:
            two_year_eps = percentage_difference(
                self.eps_year_ago, self.earnings_estimate_avg)

    def current_eps_to_estimate(self):
        if self.eps_trends.get("current") and self.earnings_estimate_avg:
            current_to_estimate = percentage_difference(
                self.eps_trends.get("current"), self.earnings_estimate_avg)

    def __gt__(self, other):
        if not self.period_year and not self.period_month and not self.period_day:
            return False
        if not other.period_year and not other.period_month and not other.period_day:
            return True
        d1 = datetime.datetime(self.period_year,
                               self.period_month,
                               self.period_day)
        d2 = datetime.datetime(other.period_year,
                               other.period_month,
                               other.period_day)
        return d1 > d2
