import json

from .yahoo_finance.api_requests import (get_analysis as api_get_analysis,
                                         get_summary as api_get_summary,
                                         get_balance_sheet as api_get_balance_sheet,
                                         get_cash_flow as api_get_cash_flow,
                                         get_earnings as api_get_earnings,
                                         get_recommendations as api_get_recommendations)

from .webscrape.scrape import (get_competitors as scrape_competitors,
                               get_latest_headlines as scrape_headlines)


class Company:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def get_competitors(self):
        self.competitors = scrape_competitors(self.name, self.symbol,
                                              self.sector, self.industry_disp,
                                              self.desc)
        f = open(f"{self.name}_competitors.txt", 'a')
        print(self.competitors)
        for comp in self.competitors:
            for key, val in comp.items():
                f.write(key+'\n')
                for v in val:
                    f.write(v + " ")
                f.write('\n')
            f.write('\n')
        f.close()

    def get_latest_headlines(self):
        self.headlines = scrape_headlines(self.name)
        f = open(f"{self.name}_headlines.txt", 'a')
        for head in self.headlines:
            f.write(head + '\n')

    def get_summary(self):
        f = open(f"{self.name}-test.txt", 'a')
        f.write("SUMMARY \n \n \n")
        response = api_get_summary(self.symbol)

        # Extract data from response
        summary_profile = response.get("summaryProfile")
        self.industry_disp = summary_profile.get("industryDisp")
        self.sector = summary_profile.get("sector")
        self.desc = summary_profile.get("longBusinessSummary")

        # Get values
        default_key_stats = response.get("defaultKeyStatistics")
        profit_margins = default_key_stats.get("profitMargins")
        delta_52_week = default_key_stats.get("52WeekChange")
        delta_sp_52_week = default_key_stats.get("SandP52WeekChange")
        shares_outstanding = default_key_stats.get("sharesOutstanding")
        shares_short = default_key_stats.get("sharesShort")
        shares_float = default_key_stats.get("floatShares")
        percent_owned_by_institutios = default_key_stats.get(
            "heldPercentInstitutions")
        price_to_book = default_key_stats.get("priceToBook")
        enterprise_value = default_key_stats.get("enterpriseValue")
        earnings_quarterly_growth = default_key_stats.get(
            "earningsQuarterlyGrowth")
        print(profit_margins)
        print(delta_52_week)
        print(delta_52_week)
        print(delta_sp_52_week)
        print(shares_outstanding)
        print(shares_short)
        print(shares_float)
        print(percent_owned_by_institutios)
        print(price_to_book)
        print(enterprise_value)
        print(earnings_quarterly_growth)
        f.write(json.dumps(response))
        f.write('\n \n \n \n')
        f.close()

    def get_analysis(self):
        f = open(f"{self.name}.txt", 'a')
        f.write("ANALYSIS \n \n \n")
        response = api_get_analysis(self.symbol)
        f.write(json.dumps(response))
        f.write('\n \n \n \n')
        f.close()

    def get_balance_sheet(self):
        f = open(f"{self.name}.txt", 'a')
        f.write("BALANCE SHEET \n \n \n")
        response = api_get_balance_sheet(self.symbol)
        f.write(json.dumps(response))
        f.write('\n \n \n \n ')
        f.close()

    def get_cash_flow(self):
        f = open(f"{self.name}.txt", 'a')
        f.write("CASH FLOW \n \n \n")
        response = api_get_cash_flow(self.symbol)
        f.write(json.dumps(response))
        f.write('\n \n \n \n')
        f.close()

    def get_earnings(self):
        f = open(f"{self.name}.txt", 'a')
        f.write("GET EARNINGS \n \n \n")
        response = api_get_earnings(self.symbol)
        f.write(json.dumps(response))
        f.write('\n \n \n \n')
        f.close()

    def get_recommendations(self):
        f = open(f"{self.name}.txt", 'a')
        f.write("RECOMMENDATIONS \n \n \n")
        response = api_get_recommendations(self.symbol)
        f.write(json.dumps(response))
        f.write('\n \n \n \n')
        f.close()


tesla = Company("tesla", "TSLA")
tesla.get_summary()
