from selenium.webdriver.common.by import By

# Container (button/link) that wraps the shopping-cart SVG
CART = (By.XPATH, "//*[local-name()='svg' and contains(@class,'lucide-shopping-cart')]/ancestor::*[self::button or self::a][1]")

# Badge with the count (round div/span with text) inside the same container
CART_BADGE = (By.XPATH, "//*[local-name()='svg' and contains(@class,'lucide-shopping-cart')]/ancestor::*[self::button or self::a][1]//*[contains(@class,'rounded-full')][normalize-space()]")
