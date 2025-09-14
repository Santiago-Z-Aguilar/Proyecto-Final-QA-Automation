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
    SHIPPING_ROW = (By.XPATH, "//div[@id='shipping-row']")
    TAX_ROW = (By.XPATH, "//div[@id='tax-row']")
    TOTAL_ROW = (By.XPATH, "//div[@id='total-row']")

    # ---------- CONFIRMATION PAGE ----------
    PURCHASE_CONFIRMATION = (By.XPATH, "//h1[text()='Order Confirmed!']")




