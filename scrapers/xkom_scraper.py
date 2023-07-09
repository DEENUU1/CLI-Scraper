import json
from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from ..database import website_exists, create_website, create_product, SessionLocal, product_exists, get_website_id
from sqlalchemy.orm import Session

db = SessionLocal()


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
    scraped_data = []
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
            product_url = driver.find_elements(By.CSS_SELECTOR, "a.sc-1h16fat-0.dNrrmO")
            for price, name, url in zip(prices, product_names, product_url):
                print(f"Product: {name.text}, Price: {price.text}, URL: {url.get_attribute('href')}")

                scraped_data.append([name.text, float(price.text.replace(",", ".")), url.get_attribute('href')])

        except Exception as e:
            print(f"Error while scraping: {str(e)}")

    driver.quit()

    return scraped_data


def xkom_save_to_database():
    """
    Save products to database
    """
    data = scrape_xkom()

    if not website_exists(db, "X-Kom"):
        create_website(db, "X-Kom")

    website_id = get_website_id(db, "X-Kom")

    for product in data:
        if not product_exists(db, product[0]):
            create_product(db, product[0], product[1], product[2], website_id)
            print(f"Product {product[0]} saved to database")
