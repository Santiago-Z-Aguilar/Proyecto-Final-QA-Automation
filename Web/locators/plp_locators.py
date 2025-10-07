from selenium.webdriver.common.by import By

class PlpLocators:

    @staticmethod
    def category_locator(category_name: str):
        # XPath dinámico para cada categoría
        return (By.XPATH, f"//img[@alt=\"{category_name}\"]")

    @staticmethod
    def category_title_locator(category_name: str):
        # XPath dinámico para el título
        return (By.XPATH, f"//h1[@id='category-title' and text()=\"{category_name}\"]")

    @staticmethod
    def category_description():
        return (By.ID, "category-description")

    # Selector del overlay/spinner
    SPINNER = (By.CSS_SELECTOR, "div.fixed.inset-0.z-50")

    # --- Locators de productos en la PLP ---
    PRODUCT_CARD = (By.CSS_SELECTOR, "div[id^='product-content-']")
    PRODUCT_IMAGE = (By.CSS_SELECTOR, "img[id^='product-image-']")
    PRODUCT_NAME = (By.CSS_SELECTOR, "h3.product-name")
    PRODUCT_DESC = (By.CSS_SELECTOR, "p.product-description")
    PRODUCT_PRICE = (By.CSS_SELECTOR, "p.product-price")
    VIEW_DETAILS_BTN = (By.CSS_SELECTOR, "button.view-details-btn")
    ADD_TO_CART_BTN = (By.CSS_SELECTOR, "button.add-to-cart-btn")

    # --- PDP ---
    @staticmethod
    def first_product():
        # Primer producto en la PLP (puede ser card o link)
        return (By.CSS_SELECTOR, "div[id^='product-content-']:first-child button.view-details-btn")

    @staticmethod
    def pdp_add_to_cart_btn():
        # Botón principal "Add to Cart" en la PDP
        return (By.CSS_SELECTOR, "button.add-to-cart-main-btn")
