import json

from ..app import (get_analysis as api_get_analysis,
                   get_summary as api_get_summary,
                   get_balance_sheet as api_get_balance_sheet,
                   get_cash_flow as api_get_cash_flow,
                   get_earnings as api_get_earnings,
                   get_recommendations as api_get_recommendations)

from ...scrape import get_competitors as scrape_competitors


class Company:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def get_competitors(self):
        self.competitors = scrape_competitors(self.name, self.symbol,
                                              self.sector, self.industry_disp,
                                              self.desc)

    def get_summary(self):
        f = open(f"{self.name}.txt", 'a')
        response = api_get_summary(self.symbol)

        # Extract data from response
        summary_profile = response.get("summaryProfile")
        self.industry_disp = summary_profile.get("industryDisp")
        self.sector = summary_profile.get("sector")
        self.desc = summary_profile.get("longBusinessSummary")
        f.write(json.dumps(response))
        f.write('\n')
        f.close()

    def get_analysis(self):
        f = open(f"{self.name}.txt", 'a')
        response = api_get_analysis(self.symbol)
        f.write(json.dumps(response))
        f.write('\n')
        f.close()

    def get_balance_sheet(self):
        f = open(f"{self.name}.txt", 'a')
        response = api_get_balance_sheet(self.symbol)
        f.write(json.dumps(response))
        f.write('\n')
        f.close()

    def get_cash_flow(self):
        f = open(f"{self.name}.txt", 'a')
        response = api_get_cash_flow(self.symbol)
        f.write(json.dumps(response))
        f.write('\n')
        f.close()

    def get_earnings(self):
        f = open(f"{self.name}.txt", 'a')
        response = api_get_earnings(self.symbol)
        f.write(json.dumps(response))
        f.write('\n')
        f.close()

    def get_recommendations(self):
        f = open(f"{self.name}.txt", 'a')
        response = api_get_recommendations(self.symbol)
        f.write(json.dumps(response))
        f.write('\n')
        f.close()
