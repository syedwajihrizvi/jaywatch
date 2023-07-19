from time import sleep
from celery import shared_task


@shared_task
def scrape_data(portfolio):
    print("Scraping for...")
    print(portfolio)
    sleep(10)
    print("Done scraping!")
