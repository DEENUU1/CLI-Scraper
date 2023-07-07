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

