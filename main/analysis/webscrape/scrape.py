import json
import codecs
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager

from ..chatgpt.bot import ask_industry, classify_headlines, get_ticker_symbol

import string

options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features')
options.add_argument('headless')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--enable-javascript")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(
    service=service, options=options)

companies = json.load(codecs.open(
    "main/analysis/webscrape/company_symbols.json", 'r', 'utf-8-sig'))
list_of_companies = companies.keys()


def get_competitors(name, symbol, api_sector, api_disp, desc):
    f = open(f"{name}-competitors.txt", "w")

    # Ask Chat GPT to get the specific sector from the company desc
    smart_industries = ask_industry(name, desc)
    industry_companies = {}

    # Google search on that sector and collect company names
    base_url = "https://www.google.com/search?q=top+consumer+"
    for industry in smart_industries:
        f.write(f"Industry: {industry}\n")
        competitors = []
        url = base_url + \
            industry.lower().replace("industry", "").replace(" ", "+")+"+companies"
        driver.get(url)

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html5lib")

        divs = soup.find_all('div', class_="B0jnne")
        for div in divs:
            competitor = div.text.lower()
            useless_part = competitor.find("ceo")
            competitor = competitor[:useless_part] if useless_part > - \
                1 else competitor
            competitor = competitor.replace("nyse:", "")
            company_symbol = find_company_symbol(competitor)
            f.write(f"{competitor}: {company_symbol} \n")
            competitors.append(company_symbol)
        industry_companies[industry] = competitors

    base_url = "https://www.google.com/search?q=top+"
    for industry in smart_industries:
        if len(industry_companies[industry]) == 0:
            f.write(f"Industry: {industry}\n")
            url = base_url + \
                industry.lower().replace("industry", "").replace(" ", "+")+"+companies"
            driver.get(url)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, "html5lib")

            divs = soup.find_all('div', class_="B0jnne")
            for div in divs:
                competitor = div.text.lower()
                useless_part = competitor.find("ceo")
                competitor = competitor[:useless_part] if useless_part > - \
                    1 else competitor
                competitor = competitor.replace("nyse:", "")
                company_symbol = find_company_symbol(competitor)
                f.write(f"{competitor}: {company_symbol} \n")
                competitors.append(company_symbol)
            industry_companies[industry] = competitors

    return industry_companies


def get_latest_headlines(name):
    url = "https://www.google.com/search?q=" + name + "&tbm=nws"
    driver.get(url)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html5lib")

    headlines = soup.find_all('div', class_="n0jPhd ynAwRc MBeuO nDgy9d")
    res = []
    for headline in headlines:
        res.append(headline.text)

    for page in range(2, 6):
        page_title = "Page " + str(page)
        pagination_item = driver.find_element(
            "css selector", f'[aria-label="{page_title}"]')
        driver.execute_script("arguments[0].click();", pagination_item)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html5lib")
        headlines = soup.find_all('div', class_="n0jPhd ynAwRc MBeuO nDgy9d")
        for headline in headlines:
            res.append(headline.text)
    classify_headlines(res, name)
    return res


def get_fund_ticker_symbol(name):
    # Option A
    url_a = f"https://www.google.com/search?q=ticker+symbol+for+{name.replace(' ', '+')}"
    driver.get(url_a)
    page_source_a = driver.page_source
    soup_a = BeautifulSoup(page_source_a, "html5lib")
    fund_name_section_a = soup_a.find('div', class_="hHq9Z")

    # Option B
    url_b = f"https://www.google.com/search?q={name.replace(' ', '+')}+ticker+symbol"
    driver.get(url_b)
    page_source_b = driver.page_source
    soup_b = BeautifulSoup(page_source_b, "html5lib")
    fund_name_section_b = soup_b.find('div', {"data-attrid": "Ticker Symbol"})

    if fund_name_section_a:
        fund_name_text = fund_name_section_a.find(
            'div', class_="iAIpCb PZPZlf").find('span', recursive=False).text
        colon_index = fund_name_text.index(':')
        fund_name = fund_name_text[colon_index+1:].replace(" ", "")
        return fund_name
    elif fund_name_section_b:
        fund_name_section_b = soup_b.find(
            'div', {"data-attrid": "Ticker Symbol"})
        fund_name = fund_name_section_b.find('span', class_="WuDkNe").text
        return fund_name
    else:
        fund_name = get_ticker_symbol(name)
        return fund_name.replace(" ", "")


def find_company_symbol(company):
    mapping_table = str.maketrans('', '', string.punctuation)
    for company_listed in list_of_companies:
        format_listed = company_listed.lower()
        extracted_listed = format_listed.translate(mapping_table)

        format_company = company.lower()
        extracted_company = format_company.translate(mapping_table)

        if company.lower() == companies[company_listed].lower():
            return companies[company_listed]
        if extracted_company == extracted_listed or extracted_company in extracted_listed or extracted_listed in extracted_company:
            return companies[company_listed]

    return "NOT_FOUND"
