import json
from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

"""
Scrape all products and prices from x-kom.pl 
"""

# Set chrome options for headless browsing
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


def get_ids() -> List[str]:
    """
    Return a list of category ids from x-kom.pl
    """
    with open("scrapers/x_kom_categories.json", 'r', encoding="utf-8") as file:
        data = json.load(file)

    ids = []

    def extract_ids(data):
        if isinstance(data, dict):
            for key, value in data.items():
                if key == 'Id':
                    ids.append(value)
                if isinstance(value, (dict, list)):
                    extract_ids(value)
        elif isinstance(data, list):
            for item in data:
                extract_ids(item)

    extract_ids(data)

    return ids


def return_all_urls():
    """
    Return all urls for every category
    """
    urls = []
    ids = get_ids()

    for id in ids:
        urls.append(f"https://www.x-kom.pl/g-2/c/{id}.html")

    return urls


def scrape_xkom():
    """
    Scrape x-kom.pl
    """

    counter = 0
    for url in return_all_urls():

        driver.get(url)

        if counter == 0:
            try:
                cookie_button = driver.find_element(By.CSS_SELECTOR, ".sc-15ih3hi-0.sc-1p1bjrl-9.dRLEBj")
                ActionChains(driver).move_to_element(cookie_button).click(cookie_button).perform()
            except Exception as e:
                print(f"Error while clicking on cookie button: {str(e)}")
        counter += 1
        try:
            prices = driver.find_elements(By.CSS_SELECTOR, 'span[data-name="productPrice"]')
            product_names = driver.find_elements(By.CSS_SELECTOR, 'h3.sc-16zrtke-0.kGLNun.sc-1yu46qn-9.feSnpB')

            for price, name in zip(prices, product_names):
                print(f"Product: {name.text}, Price: {price.text}")

        except Exception as e:
            print(f"Error while scraping: {str(e)}")

    driver.quit()
