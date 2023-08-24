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
        f = open(f"{self.name}.txt", 'a')
        f.write("SUMMARY \n \n \n")
        response = api_get_summary(self.symbol)

        # Extract data from response
        summary_profile = response.get("summaryProfile")
        self.industry_disp = self.summary_profile.get("industryDisp")
        self.sector = summary_profile.get("sector")
        self.desc = summary_profile.get("longBusinessSummary")

        # Get values
        self.market_cap = response.get("marketCap")
        default_key_stats = response.get("defaultKeyStatistics")
        self.profit_margins = default_key_stats.get("profitMargins")
        self.delta_52_week = default_key_stats.get("52WeekChange")
        self.delta_sp_52_week = default_key_stats.get("SandP52WeekChange")
        self.shares_outstanding = default_key_stats.get("sharesOutstanding")
        self.shares_short = default_key_stats.get("sharesShort")
        self.shares_float = default_key_stats.get("floatShares")
        self.shares_short_priot = default_key_stats.get(
            "sharesShortPriorMonth")
        self.percent_owned_by_institutions = default_key_stats.get(
            "heldPercentInstitutions")
        self.percent_owned_by_insiders = default_key_stats.get(
            "heldPercentInsiders")
        self.price_to_book = default_key_stats.get("priceToBook")
        self.beta = default_key_stats.get("beta")
        self.enterprise_value = default_key_stats.get("enterpriseValue")
        self.earnings_quarterly_growth = default_key_stats.get(
            "earningsQuarterlyGrowth")
        earnings = response.get("earnings")
        self.financial_charts = earnings.get('financialsChart')
        self.yearly_financial_chart = self.financial_charts.get("yearly")
        self.revenue_earnings_by_year = []
        for info in self.yearly_financial_chart:
            self.revenue_earnings_by_year.append(
                [info["date"], info["revenue"], info["earnings"]])

        fund_owners = response.get("fundOwnership")
        self.fund_owner_pct = []
        for fund in fund_owners.get("ownershipList"):
            self.fund_owner_pct.append(
                [fund["organization"], fund["pctHeld"], fund["value"]])

        insider_transactions = response.get("insiderTransactions")
        self.insider_transactions_info = []
        for transaction in insider_transactions.get("transactions"):
            self.insider_transactions_info.append([transaction.get("filerName"),
                                                   transaction.get(
                                                  "transactionText"),
                transaction.get("value"),
                transaction.get("shares"),
                transaction.get("filerRelation"),
                transaction.get("startDate")])

        key_financial_data = response.get("financialData")
        self.ebidta = key_financial_data.get("ebitda")
        self.ebidta_margins = key_financial_data.get("ebitdaMargins")
        self.gross_margins = key_financial_data.get("grossMargins")
        self.operating_cash_flow = key_financial_data.get("operatingCashflow")
        self.revenue_growth = key_financial_data.get("revenueGrowth")
        self.operating_margins = key_financial_data.get("operatingMargins")
        self.gross_profits = key_financial_data.get("grossProfits")
        self.free_cash_flow = key_financial_data.get("freeCashflow")
        self.target_median_price = key_financial_data.get("targetMedianPrice")
        self.target_mean_price = key_financial_data.get("targetMeanPrice")
        self.earnings_growth = key_financial_data.get("earningsGrowth")
        self.current_ratio = key_financial_data.get("currentRatio")
        self.return_on_assets = key_financial_data.get("returnOnAssets")
        self.return_on_equity = key_financial_data.get("returnOnEquity")
        self.debt_to_equity = key_financial_data.get("debtToEquity")
        self.total_cash = key_financial_data.get("totalCash")
        self.total_debt = key_financial_data.get("totalDebt")
        self.total_revenue = key_financial_data.get("totalRevenue")
        self.total_cash_per_share = key_financial_data.get("totalCashPerShare")
        self.revenue_per_share = key_financial_data.get("revenuePerShare")
        self.quick_ratio = key_financial_data.get("quickRatio")

        institution_ownsership = response.get("institutionOwnership")
        self.institutions = []
        for institution in institution_ownsership.get("ownershipList"):
            self.institutions.append([institution.get("organization"),
                                      institution.get("pctHeld"),
                                      institution.get("position"),
                                      institution.get("value"),
                                      institution.get("pctChange")])
        self.two_hundred_day_average = response.get("twoHundredDayAverage")
        self.fifty_day_average = response.get("fiftyDayAverage")
        self.fifty_two_week_high = response.get("fiftyTwoWeekHigh")
        self.fifty_two_week_low = response.get("fiftyTwoWeekLow")

        # Check environment existence
        esg_scores = response.get("esgScores")
        self.military_contract = esg_scores.get("militaryContract")
        self.contoversial_weapons = esg_scores.get("controversialWeapons")
        self.peer_social_performance = esg_scores.get("peerSocialPerformance")
        self.peer_environment_performance = esg_scores.get(
            "peerEnvironmentPerformance")
        self.governance_score = esg_scores.get("governanceScore")
        self.total_esg = esg_scores.get("totalEsg")

        # Upgrade/Downgrades
        upgrade_downgrade_history = response.get("upgradeDowngradeHistory")
        self.history = []
        for change in upgrade_downgrade_history.get("history")[:100]:
            # Get date after too and only get recent changes to a certain year
            self.history.append([change.get("firm"), change.get(
                "toGrade"), change.get("fromGrade")])
        f.write(json.dumps(response))
        f.write('\n \n \n \n')
        f.close()

    def get_analysis(self):
        f = open(f"{self.name}.txt", 'a')
        f.write("ANALYSIS \n \n \n")
        response = api_get_analysis(self.symbol)
        earnings_trend = response.get("earningsTrend").get("trend")
        self.earnings = []
        for earning in earnings_trend:
            self.earnings.append([earning.get("period"), earning.get("growth"), earning.get(
                "earningsEstimate"), earning.get("revenueEstimate")])
        f.write(json.dumps(response))
        f.write('\n \n \n \n')
        f.close()

    def get_balance_sheet(self):
        f = open(f"{self.name}.txt", 'a')
        f.write("BALANCE SHEET \n \n \n")
        response = api_get_balance_sheet(self.symbol)
        cash_flow_history = response.get("cashflowStatementHistory")
        self.cash_flows = []
        for cash_flow in cash_flow_history.get("cashflowStatements"):
            self.cash_flows.append([cash_flow.get("investments"),
                                    cash_flow.get("changeToLiabilities"),
                                    cash_flow.get("netBorrowings"),
                                    cash_flow.get(
                                   "totalCashFromInvestingActivities"),
                cash_flow.get(
                "totalCashFromFinancingActivities"),
                cash_flow.get(
                "totalCashFromOperatingActivities"),
                cash_flow.get("changeInCash"),
                cash_flow.get("changeToInventory"),
                cash_flow.get("changeToNetincome"),
                cash_flow.get("capitalExpenditures"),
                cash_flow.get("endDate")])

        balance_sheet_history = response.get("balanceSheetHistoryQuarterly")
        self.statements = []
        for statement in balance_sheet_history.get("balanceSheetStatements"):
            self.statements.append([statement.get("intangibleAssets"),
                                    statement.get("capitalSurplus"),
                                    statement.get("totalLiab"),
                                    statement.get("otherCurrentLiab"),
                                    statement.get("endDate"),
                                    statement.get("otherCurrentAssets"),
                                    statement.get("retainedEarnings"),
                                    statement.get("treasuryStock"),
                                    statement.get("otherAssets"),
                                    statement.get("cash"),
                                    statement.get("totalCurrentLiabilities"),
                                    statement.get("shortLongTermDebt"),
                                    statement.get("totalCurrentAssets"),
                                    statement.get("shortTermInvestments"),
                                    statement.get("longTermDebt")
                                    ])

        income_statement_history = response.get(
            "incomeStatementHistoryQuarterly")
        self.income_statements = []
        for statement in income_statement_history.get("incomeStatementHistory"):
            self.income_statements.append([statement.get("researchDevelopment"),
                                           statement.get("incomeBeforeTax"),
                                           statement.get("netIncome"),
                                           statement.get("grossProfit"),
                                           statement.get("operatingIncome"),
                                           statement.get(
                                               "otherOperatingExpenses"),
                                           statement.get("totalRevenue"),
                                           statement.get("endDate")
                                           ])
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
