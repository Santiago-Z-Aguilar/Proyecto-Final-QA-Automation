import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Web.pages.signup_page import SignUpPage
from Web.locators.header_locators import HeaderLocators
import os

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
#pytest -v -s Web/tests/slider_banner/test_slider_banner.py --browser=edge 


# Folder where screenshots will be saved
SCREENSHOTS_DIR = os.path.join(os.getcwd(), "screenshots")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook that runs after each test.
    If the test fails and the `driver` fixture exists, it saves a screenshot.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver", None)
        if driver is not None:
            # Create screenshots folder if it does not exist
            os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

            # File name = test name
            file_name = f"{report.nodeid.replace('::', '_').replace('/', '_')}.png"
            file_path = os.path.join(SCREENSHOTS_DIR, file_name)

            driver.save_screenshot(file_path)
            print(f"\n📸 Screenshot saved in: {file_path}")