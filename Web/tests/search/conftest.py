import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Web.pages.signup_page import SignUpPage
from Web.locators.header_locators import HeaderLocators



@pytest.fixture
def driver():
    # Starts browser
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)

    yield driver  # Driver is delivered to the test

    # TearDown (Runs at the end of each test)
    driver.quit()


@pytest.fixture
def navigate_to_sign_up_from_home(driver):
    """Opens home and go to the Sign-Up page clicking the Signup button """
    driver.get("https://shophub-commerce.vercel.app/")

    # Wait for the Sign-Up button to appear in the header.
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(HeaderLocators.HEADER_SIGNUP)
    )

    # Click on the Sign-Up Button
    driver.find_element(*HeaderLocators.HEADER_SIGNUP).click()

    # Wait for the Sign-Up form to load
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//div[text()='Sign Up']"))
    )

    return SignUpPage(driver)