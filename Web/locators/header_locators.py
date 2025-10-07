from selenium.webdriver.common.by import By

class HeaderLocators:
    HEADER_LOGIN = (By.XPATH, "//button[normalize-space()='Login']")
    HEADER_LOGO = (By.XPATH, "//span[text()='ShopHub']")
    HEADER_SIGNUP = (By.XPATH, "//button[text()='Sign Up']")
    CART = (By.XPATH, "//*[local-name()='svg' and contains(@class,'lucide-shopping-cart')]/ancestor::*[self::button or self::a][1]")
    CART_BADGE = (By.XPATH, "//*[local-name()='svg' and contains(@class,'lucide-shopping-cart')]/ancestor::*[self::button or self::a][1]//*[contains(@class,'rounded-full')][normalize-space()]")
    BTN_CATEGORIES = (By.XPATH, "//button[normalize-space()='Categories']")
    CATEGORY_BOOKS = (By.CSS_SELECTOR, "a[href='/categories/books']")
    OVERLAY = (By.CSS_SELECTOR, "div.fixed.inset-0.z-50")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder='Search products...']")

# --- Header / Carrito ---
    CART_ICON = (By.CSS_SELECTOR, "button.relative.h-10.w-10") # El botón del carrito
    CART_COUNT = (By.CSS_SELECTOR, "button.relative > div.absolute")  # El número de productos en el carrito