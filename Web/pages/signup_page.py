from selenium.common import TimeoutException

from .base_page import BasePage
from Web.locators.header_locators import HeaderLocators
from Web.locators.signup_locators import SignUpLocators
from Web.locators.home_locators import HomeLocators
from Web.utils.config import Config

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep

class SignUpPage(BasePage, HeaderLocators, SignUpLocators, HomeLocators):
    #URL = "https://shophub-commerce.vercel.app/"

    def load(self):
        self.visit(Config.BASE_URL)  # Usar la clase Config
        self.click(HeaderLocators.HEADER_SIGNUP)

        #print(str(HeaderLocators.HEADER_SIGNUP))

    def sign_up_as_new_user(self, fistname, lastname, email, zipcode, password):
        self.type(self.FIRST_NAME_INPUT, fistname)
        sleep(1)
        self.type(self.LAST_NAME_INPUT, lastname)
        sleep(1)
        self.type(self.EMAIL_INPUT, email)
        sleep(1)
        self.type(self.ZIPCODE_INPUT, zipcode)
        sleep(1)
        self.type(self.PASSWORD_INPUT, password)
        sleep(1)
        self.click(SignUpLocators.SUBMIT_BUTTON)

    def home_button_is_displayed_after_sign_up(self, GO_HOME_BUTTON):
        self.click(self, GO_HOME_BUTTON)
        home_after_login = self.driver.find_element(*HomeLocators.LABEL_SHOP_BY_CATEGORY)
        assert home_after_login.is_displayed()
        print("el boton go to home redirecciona a la pagina principal", home_after_login.is_displayed())
        sleep(1)

    def assert_successful_sign_up(self):
        #WebDriverWait(self.driver, 10).until()
        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(self.GO_HOME_BUTTON)
        )
        go_home_button = self.driver.find_element(*self.GO_HOME_BUTTON)
        assert go_home_button.is_displayed(), "Sign up was not successful"


    def assert_unsuccessful_sign_up(self):
        try:
            WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located(self.GO_HOME_BUTTON)
            )
            raise AssertionError("Sign up should have failed, but Go to Home button appeared.")
        except TimeoutException:
            # Si no aparece el botón, la prueba negativa pasa
            assert True

