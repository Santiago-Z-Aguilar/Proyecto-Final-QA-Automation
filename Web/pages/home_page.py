# Web/pages/home_page.py

from selenium.webdriver.support.ui import WebDriverWait
from Web.pages.base_page import BasePage
from Web.utils.config import Config
from Web.locators.home_locators import HomeLocators
from Web.locators.header_locators import HeaderLocators


class HomePage(BasePage, Config):

    def __init__(self, driver):
        super().__init__(driver)
        self.locators = HomeLocators
        self.wait = WebDriverWait(self.driver, 10)

    # ---------- NAVIGATION / LOAD ----------
    def load(self):
        """Load home page."""
        home_page_url = Config.BASE_URL
        self.visit(home_page_url)
        self.wait_for_element(self.locators.SHOP_BY_CATEGORY)

    def shop_by_category_displayed(self):
        return self.element_is_visible(self.locators.SHOP_BY_CATEGORY)

    def mens_clothes_displayed(self):
        return self.element_is_visible(self.locators.MENS_CLOTHES)

    def click_mens_clothes(self):
        return self.click(self.locators.MENS_CLOTHES)

    def women_clothes_displayed(self):
        return self.element_is_visible(self.locators.WOMEN_CLOTHES)

    def click_women_clothes(self):
        return self.click(self.locators.WOMEN_CLOTHES)

    def electronics_displayed(self):
        return self.element_is_visible(self.locators.ELECTRONICS)

    def click_electronics(self):
        return self.click(self.locators.ELECTRONICS)

    def books_displayed(self):
        return self.element_is_visible(self.locators.BOOKS)

    def click_books(self):
        return self.click(self.locators.BOOKS)

    def groceries_displayed(self):
        return self.element_is_visible(self.locators.GROCERIES)

    def click_groceries(self):
        return self.click(self.locators.GROCERIES)

    def special_deals_title_displayed(self):
        return self.element_is_visible(self.locators.SPECIAL_DEALS_TITLE)

    def view_all_deals_displayed(self):
        return self.element_is_visible(self.locators.VIEW_ALL_DEALS_BUTTON)

    def click_view_all_deals(self):
        return self.click(self.locators.VIEW_ALL_DEALS_BUTTON)

    # ---------- NAVIGATION / LOGO --------
    def wait_for_header(self):
        self.wait_for_element(HeaderLocators.HEADER_LOGO)

    def click_categories(self):
        self.click(HeaderLocators.BTN_CATEGORIES)

    def go_to_books(self):
        self.click(HeaderLocators.CATEGORY_BOOKS)

    def wait_overlay_disappear(self):
        self.wait_for_element_not_present(HeaderLocators.OVERLAY)

    def click_logo(self):
        self.click(HeaderLocators.HEADER_LOGO)

    def is_logo_displayed(self):
        return self.element_is_visible(HeaderLocators.HEADER_LOGO)