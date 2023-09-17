from time import sleep
from celery import shared_task

from .analysis.company import Company
from .analysis.portfolio import Portfolio


@shared_task
def portfolio_analysis(portfolio):
    # Go through companies in portfolio
    companies = [Company(investment["company_name"], investment["company_symbol"])
                 for investment in portfolio["investments"]]

    # Get Data
    for company in companies:
        company.get_summary()
        company.get_analysis()
        company.get_balance_sheet()

     # Analyze Data
    for company in companies:
        company.size_classification()
        company.analyze_delta()
        company.analyze_short()
        company.analyze_yearly_financials()
        company.analyze_fund_owners()
        company.analyze_insider_trading()
        company.analyze_averages()
        company.analyze_epoch()
        company.analyze_earnings()
        company.analyze_cash_flow()
        company.analyze_balance_sheet_statements()
        company.analyze_income_statements()

    # Get competitors and headlines
    for company in companies:
        company.get_competitors()
        company.get_latest_headlines()

    # Get information on competitors
    for company in companies:
        for industry, competitors in company.competitors.items():
            company_competitors = [
                Company(competitor[0], competitor[1]) for competitor in competitors]
            for competitor in company_competitors:
                competitor.get_summary()
                competitor.get_analysis()
                competitor.get_balance_sheet()
                competitor.get_latest_headlines()

    portfolio = Portfolio(companies)

    print("Finished Analysis for all companies in Portfolio")
