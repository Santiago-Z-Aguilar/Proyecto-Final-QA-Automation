from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


#Crea el driver mostrando interfaz usuario
def create_driver(headless: bool = False):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    if headless:
        options.add_argument("--headless=new")

    options.add_argument("--window-size=1920,1080")

#instanciar web driver
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options,
    )

    driver.implicitly_wait(5)
    return driver