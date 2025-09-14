# Web/pages/checkout_page.py

from selenium.webdriver.support.ui import WebDriverWait
from Web.pages.base_page import BasePage
from Web.utils.config import Config
from Web.locators.checkout_locators import CheckoutLocators
from selenium.webdriver.common.by import By
from Web.test_data.test_data import VALID_USER_CHECKOUT

class CheckoutPage(BasePage, Config):

    def __init__(self, driver):
        super().__init__(driver)
        self.locators = CheckoutLocators
        self.wait = WebDriverWait(self.driver, 10)

        # ---------- LOAD ----------

    def load(self): # A MODIFICAR CUANDO ESTE DISPONIBLE PRODUCT Y CART LOCATORS
        """Load home page."""
        men_products = Config.MEN
        self.visit(men_products)
        self.click((By.XPATH,"//button[@id='add-to-cart-2']"))
        self.click((By.XPATH,"//button[@id='add-to-cart-4']"))
        self.click((By.XPATH,"//a[@href='/cart']"))
        self.click((By.XPATH,"//a[@href='/checkout']"))
        self.wait_for_element(self.locators.TITLE)


    def fill_form(self):
        user = VALID_USER_CHECKOUT
        self.type(self.locators.FIRST_NAME, user["firstname"])
        self.type(self.locators.LAST_NAME, user["lastname"])
        self.type(self.locators.EMAIL, user["email"])
        self.type(self.locators.PHONE, user["phone"])
        self.type(self.locators.ADDRESS, user["address"])
        self.type(self.locators.CITY, user["city"])
        self.type(self.locators.ZIP_CODE, user["zipcode"])
        self.type(self.locators.COUNTRY, user["country"])

    def place_order(self):
        return self.click(self.locators.SUBMIT)

    def confirmation_displayed(self):
        return self.element_is_visible(self.locators.PURCHASE_CONFIRMATION)


