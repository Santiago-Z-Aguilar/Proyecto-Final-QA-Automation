# Web/tests/home/test_home.py

from Web.locators.home_locators import HomeLocators
from Web.utils.config import Config


# ---------- HOME BASIC VISIBILITY ----------
class TestHomeBasics:
    def test_shop_by_category_displayed(self, home_page):
        """'Shop by Category' H2 is visible."""
        home_page.load()
        assert home_page.shop_by_category_displayed(), (
            f"'Shop by Category' label not displayed. "
            f"URL: {home_page.driver.current_url} "
            f"Locator: {HomeLocators.SHOP_BY_CATEGORY}"
        )

    def test_mens_clothes_card_displayed(self, home_page):
        """Men's Clothes card is visible."""
        home_page.load()
        assert home_page.mens_clothes_displayed(), (
            f"'Men's Clothes' card not displayed. "
            f"URL: {home_page.driver.current_url} "
            f"Locator: {HomeLocators.MENS_CLOTHES}"
        )

    def test_women_clothes_card_displayed(self, home_page):
        """Women's Clothes card is visible."""
        home_page.load()
        assert home_page.women_clothes_displayed(), (
            f"'Women's Clothes' card not displayed. "
            f"URL: {home_page.driver.current_url} "
            f"Locator: {HomeLocators.WOMEN_CLOTHES}"
        )

    def test_electronics_card_displayed(self, home_page):
        """Electronics card is visible."""
        home_page.load()
        assert home_page.electronics_displayed(), (
            f"'Electronics' card not displayed. "
            f"URL: {home_page.driver.current_url} "
            f"Locator: {HomeLocators.ELECTRONICS}"
        )

    def test_books_card_displayed(self, home_page):
        """Books card is visible."""
        home_page.load()
        assert home_page.books_displayed(), (
            f"'Books' card not displayed. "
            f"URL: {home_page.driver.current_url} "
            f"Locator: {HomeLocators.BOOKS}"
        )

    def test_groceries_card_displayed(self, home_page):
        """Groceries card is visible."""
        home_page.load()
        assert home_page.groceries_displayed(), (
            f"'Groceries' card not displayed. "
            f"URL: {home_page.driver.current_url} "
            f"Locator: {HomeLocators.GROCERIES}"
        )

    def test_special_deals_title_displayed(self, home_page):
        """'Special Deals' title is visible."""
        home_page.load()
        assert home_page.special_deals_title_displayed(), (
            f"'Special Deals' title not displayed. "
            f"URL: {home_page.driver.current_url} "
            f"Locator: {HomeLocators.SPECIAL_DEALS_TITLE}"
        )

    def test_view_all_deals_button_displayed(self, home_page):
        """'View All Deals' button is visible."""
        home_page.load()
        assert home_page.view_all_deals_displayed(), (
            f"'View All Deals' button not displayed. "
            f"URL: {home_page.driver.current_url} "
            f"Locator: {HomeLocators.VIEW_ALL_DEALS_BUTTON}"
        )


# ---------- CATEGORY NAVIGATION ----------
class TestHomeNavigation:
    def test_click_mens_clothes_navigates(self, home_page):
        """Clicking Men's Clothes navigates to men category."""
        home_page.load()
        home_page.click_mens_clothes()
        assert home_page.wait_for_url_contains(Config.MEN), (
            f"Expected URL to contain '{Config.MEN}'. Current URL: {home_page.driver.current_url}"
        )

    def test_click_women_clothes_navigates(self, home_page):
        """Clicking Women's Clothes navigates to women category."""
        home_page.load()
        home_page.click_women_clothes()
        assert home_page.wait_for_url_contains(Config.WOMEN), (
            f"Expected URL to contain '{Config.WOMEN}'. Current URL: {home_page.driver.current_url}"
        )

    def test_click_electronics_navigates(self, home_page):
        """Clicking Electronics navigates to electronics category."""
        home_page.load()
        home_page.click_electronics()
        assert home_page.wait_for_url_contains(Config.ELECTRONICS), (
            f"Expected URL to contain '{Config.ELECTRONICS}'. Current URL: {home_page.driver.current_url}"
        )

    def test_click_books_navigates(self, home_page):
        """Clicking Books navigates to books category."""
        home_page.load()
        home_page.click_books()
        assert home_page.wait_for_url_contains(Config.BOOKS), (
            f"Expected URL to contain '{Config.BOOKS}'. Current URL: {home_page.driver.current_url}"
        )

    def test_click_groceries_navigates(self, home_page):
        """Clicking Groceries navigates to groceries category."""
        home_page.load()
        home_page.click_groceries()
        assert home_page.wait_for_url_contains(Config.GROCERIES), (
            f"Expected URL to contain '{Config.GROCERIES}'. Current URL: {home_page.driver.current_url}"
        )
