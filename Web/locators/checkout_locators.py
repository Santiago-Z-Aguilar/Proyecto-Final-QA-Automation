from selenium.webdriver.common.by import By

class CheckoutLocators:

    TITLE = (By.XPATH,"//div[@id='customer-info-title']")

    # ---------- CUSTOMER INFORMATION FORM ----------
    FIRST_NAME = (By.XPATH, "//input[@id='firstName']")
    LAST_NAME = (By.XPATH, "//input[@id='lastName']")
    EMAIL = (By.XPATH, "//input[@id='email']")
    PHONE = (By.XPATH, "//input[@id='phone']")
    ADDRESS = (By.XPATH, "//input[@id='address']")
    CITY = (By.XPATH, "//input[@id='city']")
    ZIP_CODE = (By.XPATH, "//input[@id='zipCode']")
    COUNTRY = (By.XPATH, "//input[@id='country']")
    SUBMIT = (By.XPATH, "//button[@id='place-order-button']")

    # ---------- ORDER INFO ----------
    ITEM_PRICES = (By.XPATH, "//p[contains(@id,'order-item-price')]")
    ITEM_QUANTITY = (By.XPATH, "//p[contains(@id,'order-item-qty')]")
    SUBTOTAL_ROW = (By.XPATH, "//div[@id='subtotal-row']")
    SUBTOTAL_PRICE = (By.XPATH, "//div[@id='subtotal-row']/span[2]")
    SHIPPING_ROW = (By.XPATH, "//div[@id='shipping-row']")
    SHIPPING_PRICE = (By.XPATH, "//div[@id='shipping-row']/span[2]")
    TAX_ROW = (By.XPATH, "//div[@id='tax-row']")
    TAX_PRICE = (By.XPATH, "//div[@id='tax-row']/span[2]")
    TOTAL_ROW = (By.XPATH, "//div[@id='total-row']")
    TOTAL_PRICE = (By.XPATH, "//div[@id='total-row']/span[2]")

    # ---------- CONFIRMATION PAGE ----------
    PURCHASE_CONFIRMATION = (By.XPATH, "//h1[text()='Order Confirmed!']")

    # ---------- CONFIRMATION PAGE ----------
    LOADING_SPINNER = (By.CSS_SELECTOR, "svg.lucide-loader-circle")




