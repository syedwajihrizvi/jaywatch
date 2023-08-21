from time import sleep
from celery import shared_task

from .analysis.company import Company
from .analysis.portfolio import Portfolio


@shared_task
def portfolio_analysis(portfolio):
    # Go through companies in portfolio
    print(portfolio)
    companies = [Company(investment["company_name"], investment["company_symbol"])
                 for investment in portfolio["investments"]]

    for company in companies:
        company.get_summary()
        company.get_analysis()
        company.get_balance_sheet()
        company.get_cash_flow()
        company.get_earnings()
        company.get_recommendations()

    # for company in companies:
    #     company.get_competitors()
    #     company.get_latest_headlines()

    # portfolio = Portfolio(companies)

    print("Finished Analysis for all companies in Portfolio")
