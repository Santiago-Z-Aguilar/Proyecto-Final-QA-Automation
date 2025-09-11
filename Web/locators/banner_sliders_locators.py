from selenium.webdriver.common.by import By

class banner_slider_Locators:
    FIRST_SLIDE = (By.XPATH, '//img[@alt="Summer Fashion Sale"]')
    SECOND_SLIDE = (By.XPATH, '//img[@alt="Latest Electronics"]')
    THIRD_SLIDE = (By.XPATH, '//img[@alt="Fresh Groceries"]')
    BUTTON_SHOPNOW_FIRST_SLIDE = (By.XPATH, "//button[text()='Order Now']") #They're the same in 3 slides
    PREVIOUS_BUTTON = (By.XPATH, '//button[.//svg[contains(@class, "lucide-chevron-left")]]')
    NEXT_BUTTON = (By.XPATH, '//button[.//svg[contains(@class, "lucide-chevron-right")]]')
    SLIDER_DOTS = (By.CSS_SELECTOR, "div.flex.space-x-2 > button")
    SLIDER_DOT_ACTIVATED = (By.CSS_SELECTOR, "div.flex.space-x-2 > button.bg-white:not(.bg-white\\/50)")
    SLIDER_DOT_NO_ACTIVATED = (By.CSS_SELECTOR, "div.flex.space-x-2 > button.bg-white\\/50")