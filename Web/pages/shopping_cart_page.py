# Web/pages/shopping_cart_page.py

from selenium.webdriver.support.ui import WebDriverWait
from Web.pages.base_page import BasePage
from Web.utils.config import Config
from Web.locators.shopping_cart_locators import ShoppingCartLocators
from Web.locators.header_locators import HeaderLocators


class ShoppingCartPage(BasePage, Config):
    """Shopping Cart Page Object."""

    def __init__(self, driver):
        super().__init__(driver)
        self.locators = ShoppingCartLocators()
        self.wait = WebDriverWait(self.driver, 10)

    # ---------- NAVIGATION ----------
    def load(self):
        """Open the cart page and wait until either the summary or empty-cart state is visible."""
        cart_url = f"{Config.BASE_URL}{Config.CART}"
        self.visit(cart_url)

    # ---------- CART BADGE ----------
    def get_cart_count(self):
        text = (self.text_of_element(HeaderLocators.CART_BADGE) or "").strip()
        return int(text) if text.isdigit() else 0

    # ---------- QUANTITY ----------
    def get_quantity(self):
        return int(self.text_of_element(self.locators.QTY_VALUE).strip())

    def _click_n(self, locator, n):
        for _ in range(max(0, n)):
            self.click(locator)

    def click_increase_quantity(self, clicks=1):
        self._click_n(self.locators.QTY_INCREMENT_BTN, clicks)
        return self.get_quantity()

    def click_decrease_quantity(self, clicks=1):
        self._click_n(self.locators.QTY_DECREMENT_BTN, clicks)
        return self.get_quantity()

    def set_quantity(self, target):
        current = self.get_quantity()
        diff = target - current
        self._click_n(self.locators.QTY_INCREMENT_BTN if diff > 0 else self.locators.QTY_DECREMENT_BTN, abs(diff))
        return self.get_quantity()

    # ---------- LINE ITEM ----------
    def remove_item(self):
        self.click(self.locators.REMOVE_BTN)

    # ---------- PRODUCT (opcional por nombre) ----------
    def product_title_displayed(self, product_name):
        return self.element_is_visible(self.locators.product_title(product_name))

    def product_image_displayed(self, product_name):
        return self.element_is_visible(self.locators.product_image_contains(product_name))

    def get_product_price_value(self):
        t = self.text_of_element(self.locators.PRODUCT_PRICE).strip()
        t = t.replace("$", "").replace(",", ".")
        return float(t)

    # ---------- ORDER SUMMARY ----------
    def get_summary_dict(self):
        to_val = lambda t: 0.0 if not t or t.strip().lower() == "free" else float(t.replace("$", "").replace(",", ".").strip())
        return {
            "subtotal": to_val(self.text_of_element(self.locators.SUBTOTAL_VALUE)),
            "shipping": to_val(self.text_of_element(self.locators.SHIPPING_VALUE)),
            "tax":      to_val(self.text_of_element(self.locators.TAX_VALUE)),
            "total":    to_val(self.text_of_element(self.locators.TOTAL_VALUE)),
        }

    # ---------- CTAs ----------
    def click_proceed_to_checkout(self):
        self.click(self.locators.PROCEED_TO_CHECKOUT_BTN)

    def click_continue_shopping(self):
        self.click(self.locators.CONTINUE_SHOPPING_BTN)


    # ---------- EMPTY CART STATE ----------
    def empty_title_visible(self):
        return self.element_is_visible(ShoppingCartLocators.EMPTY_TITLE)

    def empty_desc_visible(self):
        return self.element_is_visible(ShoppingCartLocators.EMPTY_DESC)

    def get_empty_title_text(self):
        return self.text_of_element(ShoppingCartLocators.EMPTY_TITLE)

    def get_empty_description_text(self):
        return self.text_of_element(ShoppingCartLocators.EMPTY_DESC)

    def empty_state_visible(self):
        """Convenience: título y descripción del carrito vacío visibles."""
        return self.empty_title_visible() and self.empty_desc_visible()

    def click_empty_continue_shopping(self):
        self.click(ShoppingCartLocators.EMPTY_CONTINUE_SHOPPING_BTN)
