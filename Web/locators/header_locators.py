from selenium.webdriver.common.by import By

class HeaderLocators:
    HEADER_LOGIN = (By.XPATH, "//button[normalize-space()='Login']")

    CART = (By.XPATH, "//*[local-name()='svg' and contains(@class,'lucide-shopping-cart')]/ancestor::*[self::button or self::a][1]")
    CART_BADGE = (By.XPATH, "//*[local-name()='svg' and contains(@class,'lucide-shopping-cart')]/ancestor::*[self::button or self::a][1]//*[contains(@class,'rounded-full')][normalize-space()]")
