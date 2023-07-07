from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager


class ScraperConfig:
    """
    Selenium scraper configuration class.
    """
    def __init__(self, cookie_button, url):
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.chrome_options)
        self.cookie_button = cookie_button
        self.url = url

    def get_driver(self) -> None:
        """
        Method to get the driver for selenium
        """
        self.driver.get(self.url)

    def quit_driver(self) -> None:
        """
        Method to quit the driver for selenium
        """
        self.driver.quit()

    def accept_cookies(self) -> None:
        """
        Method to accept cookies
        """
        try:
            cookie_button = self.driver.find_element(By.CSS_SELECTOR, self.cookie_button)
            ActionChains(self.driver).move_to_element(cookie_button).click(cookie_button).perform()
        except Exception as e:
            print(f"Couldn't accept cookies: {str(e)}")


URL = 'https://www.x-kom.pl/g-2/c/161-akcesoria-komputerowe.html'
config = ScraperConfig(cookie_button=".sc-15ih3hi-0.sc-1p1bjrl-9.dRLEBj", url=URL)
config.get_driver()
config.accept_cookies()

try:
    # Get the number of pages
    pages = config.driver.find_elements(By.CSS_SELECTOR, 'a.sc-1h16fat-0.sc-1xy3kzh-0.gPKgJT')
    max_page = max([int(page.get_attribute('href').split('=')[-1]) for page in pages])

    for page_number in range(1, max_page+1):
        config.driver.get(f"https://www.x-kom.pl/g-2/c/161-akcesoria-komputerowe.html?page={page_number}")
        prices = config.driver.find_elements(By.CSS_SELECTOR, 'span[data-name="productPrice"]')
        product_names = config.driver.find_elements(By.CSS_SELECTOR, 'h3.sc-16zrtke-0.kGLNun.sc-1yu46qn-9.feSnpB')

        for price, name in zip(prices, product_names):
            print(f"Product: {name.text}, Price: {price.text}")

except Exception as e:
    print(f"There was an error: {str(e)}")

config.quit_driver()
