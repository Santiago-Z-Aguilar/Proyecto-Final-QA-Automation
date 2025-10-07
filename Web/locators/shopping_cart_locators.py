from selenium.webdriver.common.by import By

class ShoppingCartLocators:
    # ---------- QUANTITY BUTTONS ----------
    QTY_DECREMENT_BTN = (By.CSS_SELECTOR, 'button:has(.lucide-minus)')
    QTY_INCREMENT_BTN = (By.CSS_SELECTOR, 'button:has(.lucide-plus)')
    QTY_VALUE = (By.CSS_SELECTOR, "span.text-center")

    # Remove button
    REMOVE_BTN = (By.XPATH, '//button[normalize-space()="Remove"]')

    # Product price (bold text)
    PRODUCT_PRICE = (By.CSS_SELECTOR, "p.font-bold")

    # Order summary
    ORDER_SUMMARY_TITLE = (By.XPATH, '//div[normalize-space()="Order Summary"]')
    SUBTOTAL_VALUE = (By.XPATH, '//div[.//span[text()="Subtotal"]]/span[2]')
    SHIPPING_VALUE = (By.XPATH, '//div[.//span[text()="Shipping"]]/span[2]')
    TAX_VALUE = (By.XPATH, '//div[.//span[text()="Tax"]]/span[2]')
    TOTAL_VALUE = (By.XPATH, '//div[.//span[text()="Total"]]/span[2]')

    # CTA buttons
    PROCEED_TO_CHECKOUT_BTN = (By.XPATH, '//button[normalize-space()="Proceed to Checkout"]')
    CONTINUE_SHOPPING_BTN = (By.XPATH, '//button[normalize-space()="Continue Shopping"]')

    # ====== Empty cart state ======
    EMPTY_TITLE = (By.XPATH, '//h1[normalize-space()="Your Cart is Empty"]')
    EMPTY_DESC = (By.XPATH, '//p[normalize-space()="Looks like you haven\'t added any items to your cart yet."]')
    EMPTY_CONTINUE_SHOPPING_BTN = (By.XPATH, '//button[normalize-space()="Continue Shopping"]')

    # ---------- DYNAMIC LOCATORS ----------
    @staticmethod
    def product_image(product_name: str):
        """Locator for <img> by exact alt text."""
        return (By.XPATH, f'//img[@alt="{product_name}"]')

    @staticmethod
    def product_image_contains(product_name: str):
        """Locator for <img> by partial alt text."""
        return (By.XPATH, f'//img[contains(@alt, "{product_name}")]')

    @staticmethod
    def product_title(product_name: str):
        """Locator for <h3> by exact text (ignores extra spaces)."""
        return (By.XPATH, f'//h3[normalize-space()="{product_name}"]')

    @staticmethod
    def product_title_contains(product_name: str):
        """Locator for <h3> by partial text match (ignores extra spaces)."""
        return (By.XPATH, f'//h3[contains(normalize-space(), "{product_name}")]')
    PAGE_TITLE = (By.XPATH, "//h1[text()='Shopping Cart']")
    PRODUCT_LIST = (By.CSS_SELECTOR, "div.cart-item")  # contenedor de cada producto, si existe
    PRODUCT_NAME = (By.CSS_SELECTOR, "h3.font-semibold")  # nombre del producto en el carrito
    PRODUCT_NAMES = (By.CSS_SELECTOR, "h3.font-semibold")  # Nombres de productos en carrito
