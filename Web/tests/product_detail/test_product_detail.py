# Web/tests/test_product_detail.py

from selenium.webdriver.common.by import By
from Web.pages.base_page import BasePage
from Web.pages.product_detail_page import ProductDetailPage
from Web.locators.product_detail_locators import ProductDetailLocators



# ---------- PDP BASIC VISIBILITY ----------
class TestPDPBasics:
    def test_product_image_display(self, product_page_class):
        """Product image is visible on PDP."""
        assert product_page_class.product_image_displayed(), (
            f"Product image not displayed. URL: {product_page_class} "
            f"Locator: {product_page_class.locators.PRODUCT_IMAGE}"
        )

    def test_product_title_display(self, product_page_class):
        """Product title is visible on PDP."""
        assert product_page_class.product_main_title_displayed(), (
            f"Product title not displayed. URL: {product_page_class.driver.current_url} "
            f"Locator: {product_page_class.locators.PRODUCT_MAIN_TITLE}"
        )

    def test_get_product_category(self, product_page_class):
        """Product category text is present on PDP."""
        assert product_page_class.get_product_category(), (
            f"Product category not displayed. URL: {product_page_class.driver.current_url} "
            f"Locator: {product_page_class.locators.PRODUCT_CATEGORY}"
        )

    def test_product_price_displayed(self, product_page_class):
        """Product price is visible on PDP."""
        assert product_page_class.product_price_displayed(), (
            f"Product price not displayed. URL: {product_page_class.driver.current_url} "
            f"Locator: {product_page_class.locators.PRODUCT_MAIN_PRICE}"
        )

    def test_product_description_display(self, product_page_class):
        """Product description text is present on PDP."""
        assert product_page_class.get_description_text(), (
            f"Product description not displayed. URL: {product_page_class.driver.current_url} "
            f"Locator: {product_page_class.locators.PRODUCT_DESCRIPTION_TEXT}"
        )

# ---------- PLP ↔ PDP CONSISTENCY ----------
class TestPLPPDPConsistency:
    def test_prices_consistency_between_plp_and_pdp(self, driver):
        base_page = BasePage(driver)
        pdp_page = ProductDetailPage(driver)

        base_page.visit("https://shophub-commerce.vercel.app/categories/men-clothes")

        plp_price_locator = (By.ID, "product-price-2")
        plp_price = base_page.text_of_element(plp_price_locator)

        view_details_locator = (By.ID, "view-details-2")
        base_page.wait_for_element(view_details_locator)
        base_page.click(view_details_locator)

        pdp_page.get_product_image()
        pdp_page.product_price_displayed()

        pdp_price = pdp_page.get_product_price_text()
        assert plp_price == pdp_price, f"PLP: {plp_price} ≠ PDP: {pdp_price}"

# ---------- QUANTITY SELECTOR ----------
class TestQuantitySelector:
    def test_quantity_selector_default_value(self, product_page):
        """Verify that the quantity selector shows the initial value as 1."""
        assert (
            product_page.get_quantity_text() == ProductDetailPage.default_quantity_products
        ), "Default quantity should be 1"

    def test_quantity_selector_increment(self, product_page):
        """Verify that the quantity increases correctly after multiple '+' clicks."""
        initial = int(product_page.get_quantity_text())
        assert product_page.click_increase_quantity(3) == str(initial + 3)

    def test_quantity_selector_decrement_above_one(self, product_page):
        """Verify that the value decreases when pressing '-' if quantity > 1."""
        quantity_after_increase = product_page.click_increase_quantity(4)  # "5"
        quantity_after_decrease = product_page.click_decrease_quantity(1)  # "4"
        expected_quantity = str(int(quantity_after_increase) - 1)
        assert quantity_after_decrease == expected_quantity, (
            f"Expected {expected_quantity}, got {quantity_after_decrease}"
        )

    def test_quantity_selector_decrement_at_one(self, product_page):
        """Verify that the value does not decrease when pressing '-' if quantity is 1."""
        # Try to decrease from 1 (should remain 1)
        assert product_page.click_decrease_quantity(3) == "1"

# ---------- CART / WISHLIST ----------
class TestCartAndWishlist:
    def test_add_to_cart_button(self, product_page):
        """Ensure the cart count matches the selected quantity after adding to cart."""
        product_page.click_increase_quantity(6)
        product_page.click_add_to_cart()
        assert product_page.get_cart_count() == 7

    def test_wishlist_icon(self, product_page):
        """Wishlist button is visible on PDP."""
        assert product_page.is_wishlist_button_displayed(), (
            f"Wishlist icon is not displayed. URL: {product_page.driver.current_url} "
            f"Locator: {product_page.locators.WISHLIST_BUTTON}"
        )

# ---------- TRUST BADGES / FEATURES ----------
class TestTrustBadges:
    def test_trust_badges(self, product_page):
        """Bulleted string in the features container matches expected text."""
        actual = product_page.get_product_features_text().strip()
        expected = ProductDetailLocators.PRODUCT_FEATURES_EXPECTED_BULLETED
        assert actual == expected, f"\nActual:\n{actual}\n\nExpected:\n{expected}"

    def test_features_container_visible(self, product_page):
        """Container for trust badges is present and visible."""
        product_page.load()
        container = product_page.get_product_features_container()
        assert (
            container is not None and container.is_displayed()
        ), "Features container not visible"

    def test_all_feature_elements_count(self, product_page):
        """There are exactly N <p> feature elements."""
        product_page.load()
        items = product_page.get_all_feature_elements()
        assert len(items) == len(ProductDetailLocators.PRODUCT_FEATURES_EXPECTED_TEXT), (
            f"Expected {len(ProductDetailLocators.PRODUCT_FEATURES_EXPECTED_TEXT)} items, "
            f"got {len(items)}"
        )

    def test_feature_texts_match_expected_exact(self, product_page):
        """Each <p> text matches the expected list (including the bullet '• ')."""
        product_page.load()
        actual = product_page.get_feature_texts()
        expected = [f"• {t}" for t in ProductDetailLocators.PRODUCT_FEATURES_EXPECTED_TEXT]
        assert actual == expected, f"\nActual:   {actual}\nExpected: {expected}"

    def test_features_text_bulleted_string_exact(self, product_page):
        """The container text matches the exact bulleted string (with newlines)."""
        product_page.load()
        actual = (product_page.get_product_features_text() or "").strip()
        expected = "• " + "\n• ".join(ProductDetailLocators.PRODUCT_FEATURES_EXPECTED_TEXT)
        assert actual == expected, f"\nActual:\n{actual}\n\nExpected:\n{expected}"

    def test_individual_feature_texts_exact(self, product_page):
        """Each individual feature text equals its expected content (with bullet)."""
        product_page.load()
        exp = ProductDetailLocators.PRODUCT_FEATURES_EXPECTED_TEXT
        assert product_page.get_shipping_feature_text() == f"• {exp[0]}"
        assert product_page.get_returns_feature_text() == f"• {exp[1]}"
        assert product_page.get_payment_feature_text() == f"• {exp[2]}"

    def test_verify_features_content(self, product_page):
        """Wrapper check: verify text contains all expected strings (no normalization needed)."""
        product_page.load()
        assert product_page.verify_features_content() is True

    def test_verify_all_features_present(self, product_page):
        """Wrapper check: verify count and each item contains expected text (order-sensitive)."""
        product_page.load()
        assert product_page.verify_all_features_present() is True

    def test_verify_individual_features(self, product_page):
        """Wrapper check: verify each feature via its specific locator."""
        product_page.load()
        assert product_page.verify_individual_features() is True
