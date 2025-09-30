from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import shutil, tempfile


#Crea el driver mostrando interfaz usuario
def create_driver(headless: bool = True):
    options = webdriver.ChromeOptions()

    if headless:
        options.add_argument("--headless=new")

    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")  # important for CI
    options.add_argument("--disable-dev-shm-usage")  # important for CI

    user_data_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={user_data_dir}")

    chrome_bin = shutil.which("google-chrome")
    if chrome_bin:
        options.binary_location = chrome_bin

#instanciar web driver
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options,
    )

    driver.implicitly_wait(5)
    return driver