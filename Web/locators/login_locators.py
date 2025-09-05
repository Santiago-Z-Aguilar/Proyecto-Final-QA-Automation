from selenium.webdriver.common.by import By

class LoginLocators:
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    #tmb funciona con el xpath "//button[@type='submit' and normalize-space()='Login']"
    GO_TO_HOME_BUTTON = (By.XPATH, "//button[text()='Go to Home']")
