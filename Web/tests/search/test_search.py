# Web/tests/search/test_search.py

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os, time

from Web.pages.home_page import HomePage

def save_screenshot(driver, name):
    os.makedirs("screenshots", exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join("screenshots", f"{name}_{timestamp}.png")
    driver.save_screenshot(path)
    print(f"\n📸 Saved in: {path}")

@pytest.mark.search
#Fails because of timeout
def test_search_laptor_redirect_fails(driver):
    """Search 'Laptop' and check its redirection fails, taking a screenshot"""
    home = HomePage(driver)
    home.load()

    #Locate input 'Search' in Home
    search_input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Search products...']")

    #Write 'Laptop' and press Enter
    search_input.send_keys("Laptop")
    search_input.send_keys(Keys.ENTER)

    #URL expected (producto - 22)
    expected_url = "https://shophub-commerce.vercel.app/product/22"

    try:
        #Waiting to change URL
        WebDriverWait(driver, 5).until(lambda d: d.current_url == expected_url)
    except Exception:
        # It does not redirect, taking screenshot
        save_screenshot(driver, "search_laptop_redirect_fail")
        raise