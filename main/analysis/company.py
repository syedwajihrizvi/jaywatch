import json
import numpy as np

from .yahoo_finance.api_requests import (get_analysis as api_get_analysis,
                                         get_summary as api_get_summary,
                                         get_balance_sheet as api_get_balance_sheet,
                                         get_cash_flow as api_get_cash_flow,
                                         get_earnings as api_get_earnings,
                                         get_recommendations as api_get_recommendations)

from .webscrape.scrape import (get_competitors as scrape_competitors,
                               get_latest_headlines as scrape_headlines)

from .utils.util import get_value_from_object, percentage_difference

LARGE_CAP = 10000000000
MID_CAP = 2000000000
SMALL_CAP = 300000000
NANO_CAP = 50000000


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
        self.industry_disp = summary_profile.get("industryDisp")
        self.sector = summary_profile.get("sector")
        self.desc = summary_profile.get("longBusinessSummary")

        # Get values
        price = response.get("price")
        self.market_cap = get_value_from_object(price, "marketCap", "raw")
        default_key_stats = response.get("defaultKeyStatistics")
        self.profit_margins = get_value_from_object(
            default_key_stats, "profitMargins", "raw")
        self.delta_52_week = get_value_from_object(
            default_key_stats, "52WeekChange", "raw")
        self.delta_sp_52_week = get_value_from_object(
            default_key_stats, "SandP52WeekChange", "raw")
        self.shares_outstanding = get_value_from_object(
            default_key_stats, "sharesOutstanding", "raw")
        self.shares_short = get_value_from_object(
            default_key_stats, "sharesShort", "raw")
        self.shares_short_prior_month = get_value_from_object(
            default_key_stats, "sharesShortPriorMonth", "raw")
        self.shares_float = get_value_from_object(
            default_key_stats, "floatShares", "raw")
        self.shares_short_prior = get_value_from_object(
            default_key_stats, "sharesShortPriorMonth", "raw")
        self.institution_count = get_value_from_object()
        self.percent_owned_by_institutions = get_value_from_object(
            default_key_stats, "heldPercentInstitutions", "raw")
        self.percent_owned_by_insiders = get_value_from_object(
            default_key_stats, "heldPercentInsiders", "raw")
        self.price_to_book = get_value_from_object(
            default_key_stats, "priceToBook", "raw")
        self.beta = get_value_from_object(default_key_stats, "beta", "raw")
        self.enterprise_value = get_value_from_object(
            default_key_stats, "enterpriseValue", "raw")
        self.earnings_quarterly_growth = get_value_from_object(
            default_key_stats, "earningsQuarterlyGrowth", "raw")
        self.peg_ratio = get_value_from_object(
            default_key_stats, "pegRatio", "raw")
        earnings = response.get("earnings")
        self.financial_charts = earnings.get('financialsChart')
        self.yearly_financial_chart = self.financial_charts.get("yearly")
        self.revenue_earnings_by_year = []
        for info in self.yearly_financial_chart:
            date = info.get("date")
            revenue = get_value_from_object(info, "revenue", "raw")
            earning = get_value_from_object(info, "earnings", "raw")
            self.revenue_earnings_by_year.append([date, revenue, earning])

        fund_owners = response.get("fundOwnership")
        self.fund_owner_pct = []
        for fund in fund_owners.get("ownershipList"):
            reportDate = get_value_from_object(fund, "reportDate", "fmt")
            organization = fund.get("organization")
            pctHeld = get_value_from_object(fund, "pctHeld", "raw")
            value = get_value_from_object(fund, "value", "raw")
            position = get_value_from_object(fund, "position", "raw")
            self.fund_owner_pct.append(
                (reportDate, organization, pctHeld, value, position))

        insider_transactions = response.get("insiderTransactions")
        self.insider_transactions_info = []
        for transaction in insider_transactions.get("transactions"):
            startDate = get_value_from_object(transaction, "startDate", "fmt")
            shares = get_value_from_object(transaction, "shares", "raw")
            transaction_value = get_value_from_object(
                transaction, "value", "raw")
            self.insider_transactions_info.append([
                transaction.get("filerName"),
                transaction.get("transactionText"),
                transaction_value,
                shares,
                transaction.get("filerRelation"),
                startDate])

        key_financial_data = response.get("financialData")
        self.ebidta = get_value_from_object(
            key_financial_data, "ebitda", "raw")
        self.ebidta_margins = get_value_from_object(
            key_financial_data, "ebitdaMargins", "raw")
        self.gross_margins = get_value_from_object(
            key_financial_data, "grossMargins", "raw")
        self.operating_cash_flow = get_value_from_object(
            key_financial_data, "operatingCashFlow", "raw")
        self.revenue_growth = get_value_from_object(
            key_financial_data, "revenueGrowth", "raw")
        self.operating_margins = get_value_from_object(
            key_financial_data, "operatingMargins", "raw")
        self.gross_profits = get_value_from_object(
            key_financial_data, "grossProfits", "raw")
        self.free_cash_flow = get_value_from_object(
            key_financial_data, "freeCashFlow", "raw")
        self.target_median_price = get_value_from_object(
            key_financial_data, "targetMedianPrice", "raw")
        self.target_mean_price = get_value_from_object(
            key_financial_data, "targetMeanPrice", "raw")
        self.earningsGrowth = get_value_from_object(
            key_financial_data, "earningsGrowth", "raw")
        self.current_ratio = get_value_from_object(
            key_financial_data, "currentRatio", "raw")
        self.return_on_assets = get_value_from_object(
            key_financial_data, "returnOnAssets", "raw")
        self.return_on_equity = get_value_from_object(
            key_financial_data, "returnOnEquity", "raw")
        self.debt_to_equity = get_value_from_object(
            key_financial_data, "debtToEquity", "raw")
        self.total_cash = get_value_from_object(
            key_financial_data, "totalCash", "raw")
        self.total_debt = get_value_from_object(
            key_financial_data, "totalDebt", "raw")
        self.total_revenue = get_value_from_object(
            key_financial_data, "totalRevenue", "raw")
        self.total_cash_per_share = get_value_from_object(
            key_financial_data, "totalCashPerShare", "raw")
        self.revenue_per_share = get_value_from_object(
            key_financial_data, "revenuePerShare", "raw")
        self.quick_ratio = get_value_from_object(
            key_financial_data, "quickRatio", "raw")

        major_holders = response.get("majorHoldersBreakdown")

        institution_ownsership = response.get("institutionOwnership")
        self.num_institutions = get_value_from_object(
            major_holders, "institutionsCount", "institutionsCount")
        self.institutions = []
        for institution in institution_ownsership.get("ownershipList"):
            # pctHeld is raw, position is raw, value is raw, reportDate is fmt, pctChange is raw
            organization = institution.get("organization")
            pctHeld = get_value_from_object(institution, "pctHeld", "raw")
            position = get_value_from_object(institution, "position", "raw")
            value = get_value_from_object(institution, "value", 'raw')
            pctChange = get_value_from_object(institution, "pctChange", "raw")
            reportDate = get_value_from_object(
                institution, "reportDate", "fmt")
            self.institutions.append([organization,
                                      pctHeld,
                                      position,
                                      value,
                                      pctChange,
                                      reportDate])
        self.two_hundred_day_average = get_value_from_object(
            response, "twoHundredDayAverage", "raw")
        self.fifty_day_average = get_value_from_object(
            response, "fiftyDayAverage", "raw")
        self.fifty_two_week_high = get_value_from_object(
            response, "fiftyTwoWeekHigh", "raw")
        self.fifty_two_week_low = get_value_from_object(
            response, "fiftyTwoWeekLow", "raw")

        # Check environment existence
        esg_scores = response.get("esgScores")
        self.military_contract = esg_scores.get("militaryContract")
        self.contoversial_weapons = esg_scores.get("controversialWeapons")
        # need min, average, max
        self.peer_social_performance = esg_scores.get("peerSocialPerformance")

        # need min, average, max
        self.peer_environment_performance = esg_scores.get(
            "peerEnvironmentPerformance")
        # raw
        self.governance_score = get_value_from_object(
            esg_scores, "governanceScore", "raw")
        self.total_esg = get_value_from_object(esg_scores, "totalEsg", "raw")

        # Upgrade/Downgrades
        upgrade_downgrade_history = response.get("upgradeDowngradeHistory")
        self.history = []
        for change in upgrade_downgrade_history.get("history")[:100]:
            # Get date after too and only get recent changes to a certain year
            self.history.append([change.get("epochGradeDate"), change.get("firm"), change.get(
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
            earnings_estimate = earning.get("earningsEstimate")
            earnings_estimate_avg = get_value_from_object(
                earnings_estimate, "avg", "raw")
            earnings_estimate_min = get_value_from_object(
                earnings_estimate, "min", "raw")
            earnings_estimate_max = get_value_from_object(
                earnings_estimate, "max", "raw")
            revenue_estimate = earning.get("revenueEstimate")
            revenue_estimate_avg = get_value_from_object(
                revenue_estimate, "avg", "raw")
            revenue_estimate_min = get_value_from_object(
                revenue_estimate, "min", "raw")
            revenue_estimate_max = get_value_from_object(
                revenue_estimate, "max", "raw")
            growth = get_value_from_object(earning, "growth", "raw")
            self.earnings.append([earning.get("endDate"),
                                  earning.get("period"),
                                  growth,
                                  earnings_estimate_avg,
                                  earnings_estimate_min,
                                  earnings_estimate_max,
                                  revenue_estimate_avg,
                                  revenue_estimate_min,
                                  revenue_estimate_max])
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
            investments = get_value_from_object(
                cash_flow, "investments", "raw")
            change_to_liabilities = get_value_from_object(
                cash_flow, "changeToLiabilities", "raw")
            net_borrowings = get_value_from_object(
                cash_flow, "netBorrowings", "raw")
            total_cash_from_investing_activities = get_value_from_object(
                cash_flow, "totalCashFromInvestingActivities", "raw")
            total_cash_from_financing_activities = get_value_from_object(
                cash_flow, "totalCashFromFinancingActivities", "raw")
            total_cash_from_operating_activities = get_value_from_object(
                cash_flow, "totalCashFromOperatingActivities", "raw")
            change_in_cash = get_value_from_object(
                cash_flow, "changeInCash", "raw")
            change_to_inventory = get_value_from_object(
                cash_flow, "changeToInventory", "raw")
            change_to_net_income = get_value_from_object(
                cash_flow, "changeToNetincome", "raw")
            capital_expenditures = get_value_from_object(
                cash_flow, "capitalExpenditures", "raw")
            end_date = get_value_from_object(cash_flow, "endDate", "raw")
            self.cash_flows.append([investments,
                                    change_to_liabilities,
                                    net_borrowings,
                                    total_cash_from_investing_activities,
                                    total_cash_from_financing_activities,
                                    total_cash_from_operating_activities,
                                    change_in_cash,
                                    change_to_inventory,
                                    change_to_net_income,
                                    capital_expenditures,
                                    end_date])

        balance_sheet_history = response.get("balanceSheetHistoryQuarterly")
        self.statements = []
        for statement in balance_sheet_history.get("balanceSheetStatements"):
            intangible_assets = get_value_from_object(
                statement, "intangibleAssets", "raw")
            capital_surplus = get_value_from_object(
                statement, "capitalSurplus", "raw")
            total_liab = get_value_from_object(statement, "totalLiab", "raw")
            other_current_liab = get_value_from_object(
                statement, "otherCurrentLiab", "raw")
            end_date = get_value_from_object(statement, "endDate", "raw")
            other_current_assets = get_value_from_object(
                statement, "otherCurrentAssets", "raw")
            retained_earnings = get_value_from_object(
                statement, "retainedEarnings", "raw")
            treasury_stock = get_value_from_object(
                statement, "treasuryStock", "raw")
            other_assets = get_value_from_object(
                statement, "otherAssets", "raw")
            cash = get_value_from_object(statement, "cash", "raw")
            total_current_liabilities = get_value_from_object(
                statement, "totalCurrentLiabilities", "raw")
            short_long_term_debt = get_value_from_object(
                statement, "shortLongTermDebt", "raw")
            total_current_assets = get_value_from_object(
                statement, "totalCurrentAssets", "raw")
            short_term_investments = get_value_from_object(
                statement, "shortTermInvestments", "raw")
            long_term_debt = get_value_from_object(
                statement, "longTermDebt", "raw")
            self.statements.append([intangible_assets,
                                    capital_surplus,
                                    total_liab,
                                    other_current_liab,
                                    end_date,
                                    other_current_assets,
                                    retained_earnings,
                                    treasury_stock,
                                    other_assets,
                                    cash,
                                    total_current_liabilities,
                                    short_long_term_debt,
                                    total_current_assets,
                                    short_term_investments,
                                    long_term_debt
                                    ])

        income_statement_history = response.get(
            "incomeStatementHistoryQuarterly")
        self.income_statements = []
        for statement in income_statement_history.get("incomeStatementHistory"):
            r_and_d = get_value_from_object(
                statement, "researchDevelopment", "raw")
            income_before_tax = get_value_from_object(
                statement, "incomeBeforeTax", "raw")
            net_income = get_value_from_object(statement, "netIncome", "raw")
            gross_profit = get_value_from_object(
                statement, "grossProfit", "raw")
            operating_income = get_value_from_object(
                statement, "operatingIncome", "raw"),
            other_operating_expenses = get_value_from_object(
                statement, "otherOperatingExpenses", "raw")
            total_revenue = get_value_from_object(
                statement, "totalRevenue", "raw")
            end_date = get_value_from_object(statement, "endDate", "fmt")
            self.income_statements.append([r_and_d,
                                           income_before_tax,
                                           net_income,
                                           gross_profit,
                                           operating_income,
                                           other_operating_expenses,
                                           total_revenue,
                                           end_date
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

    def size_classification(self):
        if self.market_cap > LARGE_CAP:
            self.company_size = "large_cap"
        elif MID_CAP <= self.market_cap <= LARGE_CAP:
            self.company_size = "mid_cap"
        elif SMALL_CAP <= self.market_cap < MID_CAP:
            self.company_size = "small_cap"
        else:
            self.company_size = "nano_cap"

    def analyze_delta(self):
        diff = percentage_difference(self.delta_52_week, self.delta_sp_52_week)
        res = ""
        if diff > 0:
            res += "positive"
        elif diff < 0:
            res += "negative"
        else:
            res += "none"

        if abs(percentage_difference) > 50:
            res += "large"
        elif 20 < abs(percentage_difference) <= 50:
            res += "medium"
        else:
            res += "low"

        self.correlation_with_s_p = res

    def analyze_short(self):
        change_in_short = percentage_difference(
            self.shares_short_prior_month, self.shares_short)
        if -30 <= change_in_short <= -10:
            self.change_in_short = "increased bearish"
        elif change_in_short < -30:
            self.change_in_short = "large bearish sentiment"
        elif 10 > change_in_short > 30:
            self.change_in_short = "bullish sentiment"
        else:
            self.change_in_short = "large bullish sentiment"

    def analyse_institution_ownership(self):
        if self.percent_owned_by_institutions > 0.5:
            self.analyze_institution = "high"
        elif 0.2 <= self.percent_owned_by_institutions <= 0.5:
            self.analyze_institution = "medium"
        else:
            self.analyze_institution = "low"

    def analyze_insider_ownership(self):
        if self.percent_owned_by_institutions > 0.5:
            self.analyze_institution = "high"
        elif 0.2 <= self.percent_owned_by_institutions <= 0.5:
            self.analyze_institution = "medium"
        else:
            self.analyze_institution = "low"

    def analyze_beta(self):
        if self.beta > 1:
            self.beta_analysis = "volatile"
        elif self.beta == 1:
            self.beta_analysis = "inline"
        elif self.beta < 1:
            self.beta_analysis = "not volatile"
        elif self.beta == 0:
            self.beta_analysis = "not associated"
        else:
            self.beta = "opposite"

    def analyze_peg_ratio(self):
        if self.peg_ratio < 1:
            self.peg_value = "undervalued"
        elif self.peg_ratio == 1:
            self.peg_value = "inline"
        else:
            self.peg_value = "overvalued"

    def analyze_yearly_financials(self):
        self.numerical_diff = []
        self.percent_diff = []
        financial_years = len(self.revenue_earnings_by_year)
        for i in range(financial_years-1):
            y1 = np.array(financial_years[i])
            y2 = np.array(financial_years[i+1])

            self.numerical_diff.append(((y2-y1)/y1))
            self.percent_diff.append(((y2-y1)/y1) * 100)

    def analyze_fund_owners(self):
        def sorter(x): return (x[3], x[2], x[4], x[0], x[1])
        sorted_fund_ownership = sorted(
            self.fund_owner_pct, sorter, reverse=True)

        top_10_funds = sorted_fund_ownership[:11]
