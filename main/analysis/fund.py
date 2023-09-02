from .yahoo_finance.api_requests import get_summary
from .utils.util import get_value_from_object


class Fund:
    def __init__(self, symbol):
        self.symbol = symbol
        self.get_fund_summary()

    def get_fund_summary(self):
        response = get_summary(self.symbol)
        default_key_statistics = response.get("defaultKeyStatistics")
        self.total_assets = get_value_from_object(
            default_key_statistics, "totalAssets", "raw")
        fund_profile = response.get("fundProfile")
        self.category = fund_profile.get("categoryName")
        top_holdings = response.get("topHoldings")
        self.holdings = [(holding.get('symbol'),
                          get_value_from_object(holding, 'holdingPercent', 'raw'))
                         for holding in top_holdings.get("holdings")]

        fund_performance = response.get('fundPerformance')
        trailing_returns = fund_performance.get('trailingReturns')
        self.three_month = get_value_from_object(
            trailing_returns, 'threeMonth', 'raw')
        self.one_year = get_value_from_object(
            trailing_returns, 'oneYear', 'raw')
        self.ytd = get_value_from_object(trailing_returns, 'ytd', 'raw')
        self.three_year = get_value_from_object(
            trailing_returns, 'threeYear', 'raw')
        self.five_year = get_value_from_object(
            trailing_returns, 'fiveYear', 'raw')

    def __str__(self):
        return f"{self.total_assets}"
