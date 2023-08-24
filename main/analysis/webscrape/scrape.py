from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager

from ..chatgpt.bot import ask_industry

options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features')
options.add_argument('headless')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--enable-javascript")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(
    service=service, options=options)


def get_competitors(name, symbol, api_sector, api_disp, desc):
    # Ask Chat GPT to get the specific sector from the company desc
    smart_industries = ask_industry(name, desc)
    industry_companies = {}

    # Google search on that sector and collect company names
    base_url = "https://www.google.com/search?q=top+consumer+"
    res = []
    for industry in smart_industries:
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
            competitors.append(competitor)
        industry_companies[industry] = competitors

    base_url = "https://www.google.com/search?q=top+"
    for industry in smart_industries:
        if len(industry_companies[industry]) == 0:
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
                competitors.append(competitor)
            industry_companies[industry] = competitors

    for industry, competitors in industry_companies.items():
        res.append({industry: competitors})

    return res


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
    return res
