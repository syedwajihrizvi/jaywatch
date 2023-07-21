from time import sleep
from celery import shared_task

from .analysis.yahoo_finance.algo.company import Company


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

    print("Finished Analysis for all companies in Portfolio")
