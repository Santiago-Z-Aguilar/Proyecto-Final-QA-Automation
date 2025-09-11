from selenium.webdriver.common.by import By

class SignUpLocators:
    FIRST_NAME_INPUT = (By.ID, "firstName")
    LAST_NAME_INPUT = (By.ID, "lastName")
    EMAIL_INPUT = (By.ID, "email")
    ZIPCODE_INPUT = (By.ID, "zipCode")
    PASSWORD_INPUT = (By.ID, "password")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "form button[type='submit']")
    GO_HOME_BUTTON = (By.XPATH, "//button[text()='Go to Home']")

