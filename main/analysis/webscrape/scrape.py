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
            competitors.append(div.text)
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

    page_2 = driver.find_element("css selector", '[aria-label="Page 2"]')
    driver.execute_script("arguments[0].click();", page_2)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html5lib")
    headlines = soup.find_all('div', class_="n0jPhd ynAwRc MBeuO nDgy9d")
    for headline in headlines:
        res.append(headline.text)
    return res
