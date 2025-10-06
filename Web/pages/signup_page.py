# Web/pages/signup_page.py

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

    def sign_up_as_new_user(self, firstname, lastname, email, zipcode, password):
        """Fill out and submit the Sign Up form"""
        self.type(self.FIRST_NAME_INPUT, firstname)
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

        # Espera hasta que el botón sea realmente clickable
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(SignUpLocators.SUBMIT_BUTTON)
        )
        submit_button = self.driver.find_element(*SignUpLocators.SUBMIT_BUTTON)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        submit_button.click()

    def assert_successful_sign_up(self):
        """Validate that the registration was successful"""
        #WebDriverWait(self.driver, 10).until()
        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(self.GO_HOME_BUTTON)
        )
        go_home_button = self.driver.find_element(*self.GO_HOME_BUTTON)
        assert go_home_button.is_displayed(), "Sign up was not successful"


    def assert_unsuccessful_sign_up(self):
        """Confirm that registration failed(Go Home button does not appear)"""
        try:
            WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located(self.GO_HOME_BUTTON)
            )
            raise AssertionError("Sign up should have failed, but Go to Home button appeared.")
        except TimeoutException:
            # Si no aparece el botón, la prueba negativa pasa
            assert True

