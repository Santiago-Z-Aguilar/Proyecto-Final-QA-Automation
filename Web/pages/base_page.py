# Web/pages/base_page.py

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Web.locators.header_locators import HeaderLocators
from selenium.webdriver import Keys


class BasePage:

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def visit(self, url: str) -> None:
        self.driver.get(url)

    def click(self, locator: tuple[By, str]):
        self.driver.find_element(*locator).click()

    def type(self, locator: tuple[By, str], text: str):
        element = self.driver.find_element(*locator)
        element.clear()
        element.send_keys(text)

    def text_of_element(self, locator: tuple[By, str]) -> str:
        return self.driver.find_element(*locator).text

    def element_is_visible(self, locator: tuple[By, str]) -> bool:
        return self.driver.find_element(*locator).is_displayed()

    def wait_for_element(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_for_elements(self, locator):
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    def wait_for_element_not_present(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(locator)
        )
    def wait_for_url_contains(self, text: str, timeout: int = 10):
        """Wait until current URL contains given text, or raise TimeoutException."""
        return WebDriverWait(self.driver, timeout).until(EC.url_contains(text))

    def search_for(self, text):
        """Writes input and press enter to search for."""
        search_input = self.wait.until(
            EC.visibility_of_element_located(HeaderLocators.SEARCH_INPUT)
        )
        search_input.clear()
        search_input.send_keys(text)
        search_input.send_keys(Keys.ENTER)