import os

from selenium.webdriver.common.devtools.v137.log import clear
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from datetime import datetime



class BasePage:

    def __init__(self, driver: WebDriver)-> None:
        self.driver = driver


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

# --- Screenshots ---
    def take_screenshot(self, test_name: str, category_name: str, suffix: str = ""):
        folder = f"screenshots/test_plp/{test_name}/"
        os.makedirs(folder, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        safe_category = category_name.replace(" ", "_").replace("'", "")
        filename = f"{test_name}_[{safe_category}]{f'_{suffix}' if suffix else ''}_{timestamp}.png"
        path = os.path.join(folder, filename)
        self.driver.save_screenshot(path)
        print(f"Screenshot guardado en: {path}")