from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from .bot import ask_industry

options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features')
options.add_argument('headless')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--enable-javascript")

service = Service(ChromeDriverManager(
    driver_version="114.0.5735.90").install())
driver = webdriver.Chrome(
    service=service, options=options)


def get_competitors(name, symbol, api_sector, api_disp, desc):
    # Ask Chat GPT to get the specific sector from the company desc
    print(f"CALLED FOR {name}")
    smart_industry = ask_industry(name, desc)
    # Google search on that sector and collect company names

    # driver.get(
    #     "https://www.google.com/search?q=top+consumer+retail+companies&client")

    # page_source = driver.page_source

    # soup = BeautifulSoup(page_source, "html5lib")
    # divs = soup.find_all('div', class_="yuRUbf")
    # for div in divs:
    #     print(div.find('h3').text)

    # print(soup.prettify())
