# Web/locators/product_detail_locators.py
from selenium.webdriver.common.by import By


class ProductDetailLocators:
    # ---------- CONTAINERS ----------
    PRODUCT_FEATURES = (By.CLASS_NAME, "product-features")

    # ---------- PDP BASIC VISIBILITY ----------
    PRODUCT_IMAGE        = (By.CLASS_NAME, "product-main-image")
    PRODUCT_MAIN_TITLE   = (By.CLASS_NAME, "product-title")
    PRODUCT_CATEGORY     = (By.CLASS_NAME, "product-category")
    PRODUCT_MAIN_PRICE   = (By.CLASS_NAME, "product-price")

    # ---------- DESCRIPTION ----------
    PRODUCT_DESCRIPTION_TITLE = (By.XPATH, "//h2[text()='Description']")
    PRODUCT_DESCRIPTION_TEXT  = (By.CLASS_NAME, "product-description")

    # ---------- QUANTITY SELECTOR ----------
    QUANTITY_DISPLAY          = (By.CLASS_NAME, "quantity-display")
    QUANTITY_DECREASE_BUTTON  = (By.CLASS_NAME, "quantity-decrease")
    QUANTITY_INCREASE_BUTTON  = (By.CLASS_NAME, "quantity-increase")

    # ---------- PRIMARY CTAs ----------
    ADD_TO_CART_BUTTON = (By.CLASS_NAME, "add-to-cart-main-btn")
    WISHLIST_BUTTON    = (By.CLASS_NAME, "wishlist-btn")

    # ---------- FEATURES (TRUST BADGES) ----------
    # By position (requires exactly three <p> in order)
    ALL_FEATURES = (By.CSS_SELECTOR, "div.product-features p")
    FEATURE_SHIPPING = (By.CSS_SELECTOR, "div.product-features p:first-child")
    FEATURE_RETURNS  = (By.CSS_SELECTOR, "div.product-features p:nth-child(2)")
    FEATURE_PAYMENT  = (By.CSS_SELECTOR, "div.product-features p:last-child")

    # ---------- EXPECTED TEXTS ----------
    PRODUCT_FEATURES_EXPECTED_TEXT = [
        "Free shipping on orders over $50",
        "30-day return policy",
        "Secure payment processing",
    ]
    PRODUCT_FEATURES_EXPECTED_BULLETED = "• " + "\n• ".join(PRODUCT_FEATURES_EXPECTED_TEXT)
