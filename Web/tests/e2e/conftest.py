import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common import TimeoutException

# Importar Page Objects
from Web.pages.base_page import BasePage
from Web.pages.home_page import HomePage
from Web.pages.signup_page import SignUpPage
from Web.pages.login_page import LoginPage
from Web.pages.product_detail_page import ProductDetailPage
from Web.pages.shopping_cart_page import ShoppingCartPage
from Web.pages.checkout_page import CheckoutPage


@pytest.fixture(scope="session")
def driver():
    """Initialize t Selenium driver for E2E testing."""
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-allow-origins=*")
    chrome_options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(25)
    yield driver
    driver.quit()


@pytest.fixture
def base_page(driver):
    return BasePage(driver)


@pytest.fixture
def home_page(driver):
    page = HomePage(driver)
    try:
        page.load()
    except TimeoutException:
        pytest.skip("Timeout charging Home Page")
    return page


@pytest.fixture
def signup_page(driver):
    page = SignUpPage(driver)
    try:
        page.load()
    except TimeoutException:
        pytest.skip("Timeout charging Sign Up Page")
    return page


@pytest.fixture
def login_page(driver):
    page = LoginPage(driver)
    try:
        page.load()
    except TimeoutException:
        pytest.skip(" Timeout charging Login Page")
    return page


@pytest.fixture
def product_page(driver):
    page = ProductDetailPage(driver)
    try:
        page.load()
    except TimeoutException:
        pytest.skip(" Timeout charging Product Detail Page")
    return page


@pytest.fixture
def shopping_cart_page(driver):
    page = ShoppingCartPage(driver)
    try:
        page.load()
    except TimeoutException:
        pytest.skip("Timeout charging Shopping Cart Page")
    return page


@pytest.fixture
def checkout_page(driver):
    page = CheckoutPage(driver)
    try:
        page.load()
    except TimeoutException:
        pytest.skip("Timeout charging Checkout Page")
    return page