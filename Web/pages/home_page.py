from Web.pages.base_page import BasePage
from Web.utils.config import Config
from Web.locators.header_locators import HeaderLocators


class HomePage(BasePage, Config):

    def __init__(self, driver):
        super().__init__(driver)

    def load(self):
        self.visit(Config.BASE_URL)

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