from selenium.common import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Web.locators.header_locators import HeaderLocators


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
