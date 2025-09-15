import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Web.locators.banner_sliders_locators import BannerSliderLocators



class BannerSliderPage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # ---------- SLIDES ----------
    def get_active_slide_src(self):
        slide = self.wait.until(
            EC.visibility_of_element_located(BannerSliderLocators.ACTIVE_SLIDE_IMG)
        )
        return slide.get_attribute("src")

    def click_next(self):
        btn = self.wait.until(EC.element_to_be_clickable(BannerSliderLocators.NEXT_BUTTON))
        btn.click()

    def click_prev(self):
        btn = self.wait.until(EC.element_to_be_clickable(BannerSliderLocators.PREV_BUTTON))
        btn.click()

    # ---------- DOTS ----------
    def get_dots(self):
        """Returns all dots in the slider"""
        return self.driver.find_elements(By.CSS_SELECTOR, "div.absolute.bottom-4 button")

    def get_active_dot_index(self):
        """Returns the index of the active dot (bg-white without /50"""
        dots = self.get_dots()
        for i, dot in enumerate(dots):
            cls = dot.get_attribute("class")
            if "bg-white/50" not in cls:  # activo = bg-white
                return i
        return -1  # no se encontró activo

    def click_dot(self, index):
        dots = self.get_dots()
        dots[index].click()
        time.sleep(1.5)  # esperar animación

    # ---------- BannerSliderPage.py ----------

    def get_active_slide_container(self):
        """Returns the container of the active slide (opacity-100)"""
        return self.driver.find_element(By.CSS_SELECTOR, "div.opacity-100")

    def get_active_slide_button(self):
        """Returns the visible button of the active slide."""
        container = self.get_active_slide_container()
        return container.find_element(By.TAG_NAME, "button")

    # ---------- SCREENSHOT ----------
    def save_slider_screenshot(self, name):
        os.makedirs("screenshots", exist_ok=True)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join("screenshots", f"{name}_{timestamp}.png")
        self.driver.save_screenshot(file_path)
        print(f"\n📸 Screenshot saved: {file_path}")

    # ---------- wait first slide ----------
    def wait_for_first_slide(self):
        return self.wait.until(
            EC.visibility_of_element_located(BannerSliderLocators.ACTIVE_SLIDE_IMG)
        )




