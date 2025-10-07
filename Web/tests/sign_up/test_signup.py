# Web/tests/shopping_cart/test_sign_up.py

import pytest
import time
from Web.pages.signup_page import SignUpPage
from Web.test_data.test_data import VALID_USER_SIGNUP, INVALID_USER_SIGNUP
from Web.locators.header_locators import HeaderLocators
from Web.utils.config import Config
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep

# Sign Up redirects correctly
def test_sign_up_button_redirects(driver):
    driver.get(Config.BASE_URL)
    driver.find_element(*HeaderLocators.HEADER_SIGNUP).click()
    WebDriverWait(driver, 10).until(EC.url_contains("/signup"))
    assert "/signup" in driver.current_url


# Sign Up is displayed
def test_sign_up_button_displayed(driver):
    driver.get(Config.BASE_URL)
    screenshot_name = f"screenshots/sign_up_button_missing_{int(time.time())}.png"

    try:
        # Wait until the button is visible
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(HeaderLocators.HEADER_SIGNUP)
        )
        button = driver.find_element(*HeaderLocators.HEADER_SIGNUP)
        assert button.is_displayed(), "Sign Up button is not visible in the DOM."

    except Exception:
        # If it fails, take a screenshot.
        driver.save_screenshot(screenshot_name)
        pytest.fail(f"Sign Up was not found on the page. Evidence saved.: {screenshot_name}")


# Sign Up does not redirect (negative)
def test_sign_up_button_does_not_redirect(driver):
    driver.get(Config.BASE_URL)
    driver.find_element(*HeaderLocators.HEADER_SIGNUP).click()

    WebDriverWait(driver, 10).until(EC.url_changes(Config.BASE_URL))
    assert "https://shophub-commerce.vercel.app/signup" not in driver.current_url, \
        f"Button redirects to /signup, it shouldnt."

# Sign Up redirects incorrectly (negative)
def test_sign_up_button_redirects_wrong(driver):
    driver.get(Config.BASE_URL)
    driver.find_element(*HeaderLocators.HEADER_SIGNUP).click()

    WebDriverWait(driver, 10).until(EC.url_changes(Config.BASE_URL))
    current_url = driver.current_url

    assert "https://shophub-commerce.vercel.app/cart" not in current_url, \
        f" Button misdirected to /cart -> {current_url}"



@pytest.mark.sign_up_validCredentials
def test_sign_up_with_valid_credentials(navigate_to_sign_up_from_home):
    #SETUP ~ Wait until the overlay disappears.
    sign_up = navigate_to_sign_up_from_home
    WebDriverWait(sign_up.driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//div[text()='Sign Up']")) #Title "Sign up"
    )
    #ACTION
    new_user = VALID_USER_SIGNUP[0]
    sign_up.sign_up_as_new_user(
        new_user["firstname"],
        new_user["lastname"],
        new_user["email"],
        new_user["zipcode"],
        new_user["password"])

    # Wait until the overlay disappears.
    WebDriverWait(sign_up.driver,20 ).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Sign Up']"))
    )
    #ASSERTION
    sign_up.assert_successful_sign_up()

def test_sign_up_number_as_password(navigate_to_sign_up_from_home):
    #SETUP
    #Wait until the overlay disappears.
    sign_up = navigate_to_sign_up_from_home
    WebDriverWait(sign_up.driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//div[text()='Sign Up']")) #Title "Sign up"
    )
    #ACTION
    new_user = VALID_USER_SIGNUP[1]
    sign_up.sign_up_as_new_user(
        new_user["firstname"],
        new_user["lastname"],
        new_user["email"],
        new_user["zipcode"],
        new_user["password"])
    # Wait until the overlay disappears.
    WebDriverWait(sign_up.driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//button[text()='Sign Up']"))
    )
    # ASSERTION
    sign_up.assert_successful_sign_up()

#Email already registered - It should fail
def test_sign_up_email_already_registered(navigate_to_sign_up_from_home):
    #SETUP
    #Wait until the overlay disappears.
    sign_up = navigate_to_sign_up_from_home
    WebDriverWait(sign_up.driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//div[text()='Sign Up']")) #Title "Sign up"
    )
    #ACTION
    new_user = INVALID_USER_SIGNUP[0]
    sign_up.sign_up_as_new_user(
        new_user["firstname"],
        new_user["lastname"],
        new_user["email"],
        new_user["zipcode"],
        new_user["password"])
    # Wait until the overlay disappears.
    WebDriverWait(sign_up.driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//button[text()='Sign Up']"))
    )
    # ASSERTION
    sign_up.assert_unsuccessful_sign_up()


#Number as name and lastname
def test_sign_up_numbers_as_names(navigate_to_sign_up_from_home):
    #SETUP
    #Wait until the overlay disappears.
    sign_up = navigate_to_sign_up_from_home
    WebDriverWait(sign_up.driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//div[text()='Sign Up']")) #Title "Sign up"
    )
    #ACTION
    new_user = INVALID_USER_SIGNUP[1]
    sign_up.sign_up_as_new_user(
        new_user["firstname"],
        new_user["lastname"],
        new_user["email"],
        new_user["zipcode"],
        new_user["password"])
    # Wait until the overlay disappears.
    WebDriverWait(sign_up.driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//button[text()='Sign Up']"))
    )
    # ASSERTION
    sign_up.assert_unsuccessful_sign_up()


#Empty email
def test_sign_up_empty_email(navigate_to_sign_up_from_home):
    #SETUP
    #Wait until the overlay disappears.
    sign_up = navigate_to_sign_up_from_home
    WebDriverWait(sign_up.driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//div[text()='Sign Up']")) #Title "Sign up"
    )
    #ACTION
    new_user = INVALID_USER_SIGNUP[2]
    sign_up.sign_up_as_new_user(
        new_user["firstname"],
        new_user["lastname"],
        new_user["email"],
        new_user["zipcode"],
        new_user["password"])
    # Wait until the overlay disappears.
    WebDriverWait(sign_up.driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//button[text()='Sign Up']"))
    )
    # ASSERTION
    sign_up.assert_unsuccessful_sign_up()


#String as zipcode
def test_sign_up_string_as_zipcode(navigate_to_sign_up_from_home):
    #SETUP
    #Wait until the overlay disappears.
    sign_up = navigate_to_sign_up_from_home
    WebDriverWait(sign_up.driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//div[text()='Sign Up']")) #Title "Sign up"
    )
    #ACTION
    new_user = INVALID_USER_SIGNUP[3]
    sign_up.sign_up_as_new_user(
        new_user["firstname"],
        new_user["lastname"],
        new_user["email"],
        new_user["zipcode"],
        new_user["password"])
    # Wait until the overlay disappears.
    WebDriverWait(sign_up.driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//button[text()='Sign Up']"))
    )
    # ASSERTION
    sign_up.assert_unsuccessful_sign_up()


#Invalid email format
def test_sign_up_invalid_email_format(navigate_to_sign_up_from_home):
    #SETUP
    #Wait until the overlay disappears.
    sign_up = navigate_to_sign_up_from_home
    WebDriverWait(sign_up.driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//div[text()='Sign Up']")) #Title "Sign up"
    )
    #ACTION
    new_user = INVALID_USER_SIGNUP[4]
    sign_up.sign_up_as_new_user(
        new_user["firstname"],
        new_user["lastname"],
        new_user["email"],
        new_user["zipcode"],
        new_user["password"])
    # Wait until the overlay disappears.
    WebDriverWait(sign_up.driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//button[text()='Sign Up']"))
    )
    # ASSERTION
    sign_up.assert_unsuccessful_sign_up()

#Email without domain
def test_sign_up_email_without_domain(navigate_to_sign_up_from_home):
    #SETUP
    #Wait until the overlay disappears.
    sign_up = navigate_to_sign_up_from_home
    WebDriverWait(sign_up.driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//div[text()='Sign Up']")) #Title "Sign up"
    )
    #ACTION
    new_user = INVALID_USER_SIGNUP[5]
    sign_up.sign_up_as_new_user(
        new_user["firstname"],
        new_user["lastname"],
        new_user["email"],
        new_user["zipcode"],
        new_user["password"])
    # Wait until the overlay disappears.
    WebDriverWait(sign_up.driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//button[text()='Sign Up']"))
    )
    # ASSERTION
    sign_up.assert_unsuccessful_sign_up()


#Empty all credentials
def test_sign_up_empty_all_credentials(navigate_to_sign_up_from_home):
    #SETUP
    #Wait until the overlay disappears.
    sign_up = navigate_to_sign_up_from_home
    WebDriverWait(sign_up.driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//div[text()='Sign Up']")) #Title "Sign up"
    )
    #ACTION
    new_user = INVALID_USER_SIGNUP[6]
    sign_up.sign_up_as_new_user(
        new_user["firstname"],
        new_user["lastname"],
        new_user["email"],
        new_user["zipcode"],
        new_user["password"])
    # Wait until the overlay disappears.
    WebDriverWait(sign_up.driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//button[text()='Sign Up']"))
    )
    # ASSERTION
    sign_up.assert_unsuccessful_sign_up()


#All invalid credentials
def test_sign_up_all_invalid_credentials(navigate_to_sign_up_from_home):
    #SETUP
    #Wait until the overlay disappears.
    sign_up = navigate_to_sign_up_from_home
    WebDriverWait(sign_up.driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//div[text()='Sign Up']")) #Title "Sign up"
    )
    #ACTION
    new_user = INVALID_USER_SIGNUP[7]
    sign_up.sign_up_as_new_user(
        new_user["firstname"],
        new_user["lastname"],
        new_user["email"],
        new_user["zipcode"],
        new_user["password"])
    # Wait until the overlay disappears.
    WebDriverWait(sign_up.driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//button[text()='Sign Up']"))
    )
    # ASSERTION
    sign_up.assert_unsuccessful_sign_up()