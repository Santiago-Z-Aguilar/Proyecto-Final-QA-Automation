from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import shutil, tempfile, subprocess, re, sys, os



def _find_chrome_binary():
    # Linux CI: "google-chrome" is installed
    if sys.platform.startswith("linux"):
        return shutil.which("google-chrome")
    # macOS
    if sys.platform == "darwin":
        return "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

    return None


#Crea el driver mostrando interfaz usuario
def create_driver(headless: bool = True):
    options = webdriver.ChromeOptions()

    if headless:
        options.add_argument("--headless=new")

    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")  # important for CI
    options.add_argument("--disable-dev-shm-usage")  # important for CI
    options.add_argument("--homepage=about:blank")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")

    user_data_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={user_data_dir}")

    chrome_bin = _find_chrome_binary()
    if chrome_bin:
        options.binary_location = chrome_bin

        chrome_version = subprocess.check_output([chrome_bin, "--version"]).decode()
        major_version = re.search(r"\d+", chrome_version).group()
        driver_path = ChromeDriverManager(version=major_version).install()
    else:
        driver_path = ChromeDriverManager().install()


#instanciar web driver
    driver = webdriver.Chrome(
        service=ChromeService(driver_path),
        options=options,
    )
    driver.implicitly_wait(5)
    return driver