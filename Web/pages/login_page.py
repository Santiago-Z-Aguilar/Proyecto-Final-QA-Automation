from .base_page import BasePage
from Web.locators.header_locators import HeaderLocators
from Web.locators.login_locators import LoginLocators
from Web.locators.home_locators import HomeLocators
from Web.utils.config import Config

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep

class LoginPage(BasePage, HeaderLocators, LoginLocators, Config, HomeLocators):
    #Datos
    #URL = "https://shophub-commerce.vercel.app/"

    #Selectores
   # HEADER_LOGIN = (By.XPATH, "//button[normalize-space()='Login']")

    def load(self):
        self.visit(self.BASE_URL)

        sleep(2)
        self.click(self.HEADER_LOGIN)

        print(str(HeaderLocators.HEADER_LOGIN))

    def login_as_user(self, username, password):
        # Espera hasta que el overlay desaparezca
        #WebDriverWait(self.driver, 10).until(
         #   EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.fixed.inset-0.z-50"))
        #)
        self.type(self.EMAIL_INPUT, username)
        sleep(1)
        self.type(self.PASSWORD_INPUT, password)
        sleep(1)
        self.click(self.LOGIN_BUTTON)
        sleep(1)

    def assert_home_button_after_login(self):
        self.click(self.GO_TO_HOME_BUTTON)
        home_after_login = self.driver.find_element(*HomeLocators.LABEL_SHOP_BY_CATEGORY)
        assert home_after_login.is_displayed()
        print("el boton go to home redirecciona a la pagina principal", home_after_login.is_displayed())
        sleep(1)

    def assert_successful_login(self):
        #WebDriverWait(self.driver, 10).until()
        assert "success" in self.driver.current_url, "Login was not successful"

    def assert_unsuccessful_login(self):
        logged_user = self.driver.execute_script("return window.localStorage.getItem('loggedInUser');")
        assert logged_user is None
        print("EVALUA", logged_user)
