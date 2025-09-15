# Web/pages/checkout_page.py
from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from Web.pages.base_page import BasePage
from Web.utils.config import Config
from Web.locators.checkout_locators import CheckoutLocators
from selenium.webdriver.common.by import By
from Web.test_data.test_data import VALID_USER_CHECKOUT
from selenium.webdriver.common.alert import Alert

class CheckoutPage(BasePage, Config):

    def __init__(self, driver):
        super().__init__(driver)
        self.locators = CheckoutLocators
        self.wait = WebDriverWait(self.driver, 10)

        # ---------- LOAD ----------

    def load(self): # A MODIFICAR CUANDO ESTE DISPONIBLE PRODUCT Y CART LOCATORS
        """Load checkout page."""
        book_products = Config.BASE_URL + Config.BOOKS
        self.visit(book_products)
        self.click((By.XPATH,"//button[@id='add-to-cart-31']"))
        self.click((By.XPATH,"//button[@id='add-to-cart-32']"))
        self.wait_for_invisibility(self.locators.LOADING_SPINNER)
        self.click((By.XPATH,"//a[@href='/cart']"))
        self.wait_for_invisibility(self.locators.LOADING_SPINNER)
        self.click((By.XPATH,"//a[@href='/checkout']"))
        self.wait_for_invisibility(self.locators.LOADING_SPINNER)
        self.wait_for_element(self.locators.TITLE)

    def fill_form(self,user_data, skip: list[str] = None):
        """Fill the form, skipping any fields passed in skip list"""
        if skip is None:
            skip = []
        user = user_data
        field_mapping = {
            "firstname": self.locators.FIRST_NAME,
            "lastname": self.locators.LAST_NAME,
            "email": self.locators.EMAIL,
            "phone": self.locators.PHONE,
            "address": self.locators.ADDRESS,
            "city": self.locators.CITY,
            "zipcode": self.locators.ZIP_CODE,
            "country": self.locators.COUNTRY,
        }
        for field, locator in field_mapping.items():
            if field not in skip:
                self.type(locator, user[field])

    def place_order(self):
        return self.click(self.locators.SUBMIT)

    def confirmation_displayed(self):
        return self.element_is_visible(self.locators.PURCHASE_CONFIRMATION)

    def confirmation_page_loaded(self):
        return self.wait_for_url_contains(Config.CONFIRMATION)

    def is_alert_present(self):
        try:
            self.wait_for_alert()
            return True
        except TimeoutException:
            return False

    def get_alert_text(self):
        if self.is_alert_present():
            alert = self.driver.switch_to.alert
            return alert.text
        return None

    def get_validation_message(self):
        email_input = self.wait_for_element(self.locators.EMAIL)
        return email_input.get_attribute('validationMessage')


