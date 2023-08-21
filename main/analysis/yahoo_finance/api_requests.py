import requests

headers = headers = {
    "X-RapidAPI-Key": "1ecf9f88d4msh40a78a6c5f89f74p1dfc3cjsn1b9a26cc7e5e",
    "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
}

BALANCE_SHEET_URL = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-balance-sheet"
CASH_FLOW_URL = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-cash-flow"
SUMMARY_URL = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-summary"
EARNINGS_URL = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/get-earnings"
RECOMMENDATIONS_URL = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-recommendations"
ANALYSIS_URL = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-analysis"


def get_summary(symbol):
    querystring = {"symbol": symbol, "region": "US"}

    response = requests.get(
        SUMMARY_URL, headers=headers, params=querystring)
    return response.json()


def get_analysis(symbol):
    querystring = {"symbol": symbol, "region": "US"}

    response = requests.get(
        ANALYSIS_URL, headers=headers, params=querystring)

    return response.json()


def get_balance_sheet(symbol):

    querystring = {"symbol": symbol, "region": "US"}

    response = requests.get(
        BALANCE_SHEET_URL, headers=headers, params=querystring)

    return response.json()


def get_cash_flow(symbol):
    querystring = {"symbol": symbol, "region": "US"}

    response = requests.get(
        CASH_FLOW_URL, headers=headers, params=querystring)

    return response.json()


def get_earnings(symbol):
    querystring = {"symbol": symbol, "region": "US"}

    response = requests.get(
        EARNINGS_URL, headers=headers, params=querystring)

    return response.json()


def get_recommendations(symbol):
    querystring = {"symbol": symbol, "region": "US"}

    response = requests.get(
        RECOMMENDATIONS_URL, headers=headers, params=querystring)

    return response.json()
