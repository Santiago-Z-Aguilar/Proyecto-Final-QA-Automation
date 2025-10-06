from selenium.webdriver.common.by import By

class HeaderLocators:
    HEADER_LOGIN = (By.XPATH, "//button[normalize-space()='Login']")

# --- Header / Carrito ---
    CART_ICON = (By.CSS_SELECTOR, "button.relative.h-10.w-10") # El botón del carrito
    CART_COUNT = (By.CSS_SELECTOR, "button.relative > div.absolute")  # El número de productos en el carrito