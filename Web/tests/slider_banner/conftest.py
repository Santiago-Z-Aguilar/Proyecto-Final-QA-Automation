import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Web.pages.signup_page import SignUpPage
from Web.locators.header_locators import HeaderLocators
import os

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--incognito")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()




# Carpeta donde se guardarán los screenshots
SCREENSHOTS_DIR = os.path.join(os.getcwd(), "screenshots")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook de pytest que se ejecuta después de cada test.
    Si el test falla y existe el fixture `driver`, guarda un screenshot.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver", None)
        if driver is not None:
            # Crear carpeta screenshots si no existe
            os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

            # Nombre del archivo = nombre del test
            file_name = f"{report.nodeid.replace('::', '_').replace('/', '_')}.png"
            file_path = os.path.join(SCREENSHOTS_DIR, file_name)

            driver.save_screenshot(file_path)
            print(f"\n📸 Screenshot guardado en: {file_path}")