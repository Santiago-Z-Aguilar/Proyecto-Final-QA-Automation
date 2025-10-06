# Web/pages/checkout_page.py
from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from Web.pages.base_page import BasePage
from Web.utils.config import Config
from Web.locators.checkout_locators import CheckoutLocators
from selenium.webdriver.common.by import By
import re

class CheckoutPage(BasePage, Config):

    def __init__(self, driver):
        super().__init__(driver)
        self.locators = CheckoutLocators
        self.wait = WebDriverWait(self.driver, 10)

    def _extract_number_from_text(self,text):
        result = re.search(r"[\d.]+",text)
        if result:
            return float(result.group())
        else:
            return 0

    # ---------- LOAD ----------
    def load(self): # A MODIFICAR CUANDO ESTE DISPONIBLE PRODUCT Y CART LOCATORS
        """Load checkout page."""
        book_products = Config.BASE_URL + Config.BOOKS
        self.visit(book_products)
        self.click((By.XPATH,"//button[@id='add-to-cart-31']"))
        self.click((By.XPATH,"//button[@id='add-to-cart-32']"))
        self.click((By.XPATH,"//a[@href='/cart']"))
        self.wait_for_element_not_present(self.locators.LOADING_SPINNER)
        self.click((By.XPATH,"//a[@href='/checkout']"))
        self.wait_for_element_not_present(self.locators.LOADING_SPINNER)

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

    def is_product_price_displayed(self):
        product_prices = self.wait_for_elements(self.locators.ITEM_PRICES)
        return product_prices is not None

    def is_subtotal_displayed(self):
        return self.element_is_visible(self.locators.SUBTOTAL_ROW)

    def is_shipping_displayed(self):
        return self.element_is_visible(self.locators.SHIPPING_ROW)

    def is_tax_displayed(self):
        return self.element_is_visible(self.locators.TAX_ROW)

    def subtotal_calculation(self):
        subtotal = 0
        item_prices = self.wait_for_elements(self.locators.ITEM_PRICES)
        for price_elem in item_prices:
            price = self._extract_number_from_text(price_elem.text)
            subtotal += price
        return subtotal

    def get_subtotal_price(self):
        subtotal_price = self.text_of_element(self.locators.SUBTOTAL_PRICE)
        return self._extract_number_from_text(subtotal_price)

    def get_shipping_price(self):
        shipping_price = self.text_of_element(self.locators.SHIPPING_PRICE)
        return self._extract_number_from_text(shipping_price)

    def get_tax_price(self):
        tax_price = self.text_of_element(self.locators.TAX_PRICE)
        return self._extract_number_from_text(tax_price)

    def total_calculation(self):
        subtotal = self.get_subtotal_price()
        shipping = self.get_shipping_price()
        tax = self.get_tax_price()
        return subtotal + shipping + tax

    def get_total_price(self):
        total_price = self.text_of_element(self.locators.TOTAL_PRICE)
        return self._extract_number_from_text(total_price)







