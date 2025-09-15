# Web/pages/product_detail_page.py

from selenium.webdriver.support.ui import WebDriverWait
from Web.locators.header_locators import HeaderLocators
from Web.pages.base_page import BasePage
from Web.locators.product_detail_locators import ProductDetailLocators
from Web.utils.config import Config
from Web.test_data.products import *

class ProductDetailPage(BasePage, Config):
    product_id_to_test = PRODUCTS[DENIM_JEANS]["id"]
    default_quantity_products = "1"

    def __init__(self, driver):
        super().__init__(driver)
        self.locators = ProductDetailLocators()
        self.wait = WebDriverWait(self.driver, 10)

    # ---------- NAVIGATION / LOAD ----------
    def load(self, product_id=None):
        """Load product page using product id."""
        product_id_to_use = product_id if product_id is not None else self.product_id_to_test
        product_detail_url = f"{Config.BASE_URL}{Config.PRODUCT_DETAIL}{product_id_to_use}"
        self.visit(product_detail_url)
        self.wait_for_element(self.locators.PRODUCT_FEATURES)

    # ---------- PDP BASIC VISIBILITY ----------
    def get_product_image(self):
        return self.wait_for_element(self.locators.PRODUCT_IMAGE)

    def product_image_displayed(self):
        return self.element_is_visible(self.locators.PRODUCT_IMAGE)

    def product_main_title_displayed(self):
        return self.element_is_visible(self.locators.PRODUCT_MAIN_TITLE)

    # ---------- PDP PRODUCT INFO ----------
    def get_product_category(self):
        return self.text_of_element(self.locators.PRODUCT_CATEGORY)

    def product_price_displayed(self):
        return self.element_is_visible(self.locators.PRODUCT_MAIN_PRICE)

    def get_product_price_text(self):
        return self.text_of_element(self.locators.PRODUCT_MAIN_PRICE)

    def get_description_title(self):
        return self.text_of_element(self.locators.PRODUCT_DESCRIPTION_TITLE)

    def get_description_text(self):
        return self.text_of_element(self.locators.PRODUCT_DESCRIPTION_TEXT)

    # ---------- QUANTITY SELECTOR ----------
    def get_quantity_text(self):
        return self.text_of_element(self.locators.QUANTITY_DISPLAY)

    def click_increase_quantity(self, clicks=1):
        """Increase quantity by clicking '+' button specified number of times."""
        for _ in range(clicks):
            self.click(self.locators.QUANTITY_INCREASE_BUTTON)
        return self.get_quantity_text()

    def click_decrease_quantity(self, clicks=1):
        """Decrease quantity by clicking '-' button specified number of times."""
        for _ in range(clicks):
            self.click(self.locators.QUANTITY_DECREASE_BUTTON)
        return self.get_quantity_text()

    def are_quantity_buttons_displayed(self):
        return (
            self.element_is_visible(self.locators.QUANTITY_DECREASE_BUTTON)
            and self.element_is_visible(self.locators.QUANTITY_INCREASE_BUTTON)
        )

    # ---------- CART / WISHLIST ----------
    def is_add_to_cart_button_displayed(self):
        return self.element_is_visible(self.locators.ADD_TO_CART_BUTTON)

    def click_add_to_cart(self):
        self.click(self.locators.ADD_TO_CART_BUTTON)

    def get_cart_count(self) -> int:
        """Return the cart items count; 0 if badge is missing or empty."""
        try:
            return int(self.text_of_element(HeaderLocators.CART_BADGE))
        except Exception:
            return 0

    def is_wishlist_button_displayed(self):
        return self.element_is_visible(self.locators.WISHLIST_BUTTON)

    def click_wishlist(self):
        self.click(self.locators.WISHLIST_BUTTON)

    # ---------- TRUST BADGES / FEATURES ----------
    def get_product_features_container(self):
        return self.wait_for_element(self.locators.PRODUCT_FEATURES)

    def get_product_features_text(self):
        return self.text_of_element(self.locators.PRODUCT_FEATURES)

    def get_all_feature_elements(self):
        return self.wait_for_elements(self.locators.ALL_FEATURES)

    def get_feature_texts(self):
        features = self.get_all_feature_elements()
        return [feature.text for feature in features]

    def get_shipping_feature_text(self):
        return self.text_of_element(self.locators.FEATURE_SHIPPING)

    def get_returns_feature_text(self):
        return self.text_of_element(self.locators.FEATURE_RETURNS)

    def get_payment_feature_text(self):
        return self.text_of_element(self.locators.FEATURE_PAYMENT)

    def verify_features_content(self):
        """Verify expected text in features (container string contains all)."""
        features_text = self.get_product_features_text()
        for expected_text in self.locators.PRODUCT_FEATURES_EXPECTED_TEXT:
            if expected_text not in features_text:
                return False
        return True

    def verify_all_features_present(self):
        """Verify all features are present and contain expected text (order-sensitive)."""
        try:
            feature_texts = self.get_feature_texts()
            if len(feature_texts) != len(self.locators.PRODUCT_FEATURES_EXPECTED_TEXT):
                return False
            for i, feature_text in enumerate(feature_texts):
                expected = self.locators.PRODUCT_FEATURES_EXPECTED_TEXT[i]
                if expected not in feature_text:
                    return False
            return True
        except:
            return False

    def verify_individual_features(self):
        """Verify individual features by specific CSS locators."""
        try:
            shipping_text = self.get_shipping_feature_text()
            returns_text = self.get_returns_feature_text()
            payment_text = self.get_payment_feature_text()
            return (
                self.locators.PRODUCT_FEATURES_EXPECTED_TEXT[0] in shipping_text
                and self.locators.PRODUCT_FEATURES_EXPECTED_TEXT[1] in returns_text
                and self.locators.PRODUCT_FEATURES_EXPECTED_TEXT[2] in payment_text
            )
        except:
            return False
