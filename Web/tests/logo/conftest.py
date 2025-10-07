import pytest
from selenium import webdriver

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

#pytest -v -s Web/tests/logo/test_logo.py --browser=edge
