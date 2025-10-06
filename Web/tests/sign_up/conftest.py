import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Web.pages.signup_page import SignUpPage
from Web.locators.header_locators import HeaderLocators



def pytest_addoption(parser):
    print(">>> conftest.py CHARGED <<<")   # debug
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to use: chrome or edge"
    )

@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser").lower()

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--incognito")
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)

    elif browser == "edge":
        options = webdriver.EdgeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--inprivate")
        driver = webdriver.Edge(options=options)

    else:
        raise ValueError(f"Browser no supported: {browser}")

    driver.implicitly_wait(10)
    yield driver
    driver.quit()

#Choose browser in console
#pytest -v -s Web/tests/sign_up/test_signup.py --browser=edge


@pytest.fixture
def navigate_to_sign_up_from_home(driver):
    #Opens home and go to the Sign-Up page clicking header button
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