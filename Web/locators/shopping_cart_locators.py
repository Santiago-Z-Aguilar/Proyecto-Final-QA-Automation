from selenium.webdriver.common.by import By

class ShoppingCartLocators:
    PAGE_TITLE = (By.XPATH, "//h1[text()='Shopping Cart']")
    PRODUCT_LIST = (By.CSS_SELECTOR, "div.cart-item")  # contenedor de cada producto, si existe
    PRODUCT_NAME = (By.CSS_SELECTOR, "h3.font-semibold")  # nombre del producto en el carrito
    PRODUCT_NAMES = (By.CSS_SELECTOR, "h3.font-semibold")  # Nombres de productos en carrito
