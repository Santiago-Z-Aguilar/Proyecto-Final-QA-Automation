from selenium.webdriver.common.by import By


class BannerSliderLocators:
    ACTIVE_SLIDE_IMG = (By.CSS_SELECTOR, "div.opacity-100 img")
    ALL_SLIDES = (By.CSS_SELECTOR, "div.transition-opacity img")

    NEXT_BUTTON = (
        By.CSS_SELECTOR,
        "button[aria-label='Next'], button.right-4, button:has(svg.lucide-chevron-right)"
    )
    PREV_BUTTON = (By.CSS_SELECTOR,
        "button[aria-label='Previous'], button.left-4, button:has(svg.lucide-chevron-left)"
    )

    SLIDER_DOTS = (By.CSS_SELECTOR, "div.flex.space-x-2 button")
    SLIDER_DOT_ACTIVE = (By.CSS_SELECTOR, "div.flex.space-x-2 button.bg-white")  # activo

    #Redirections and Buttons
    ACTIVE_SLIDE_BUTTON = (By.TAG_NAME, "button")

    CLOTHES_REDIRECTION = (By.XPATH, "//h1[normalize-space(text())=\"Men's Clothes\"]") #Men's clothes title
    ELECTRONICS_REDIRECTION = (By.XPATH, "//h1[normalize-space(text())='Electronics']") #Electronics title
    GROCERIES_REDIRECTION = (By.XPATH, "//h1[normalize-space(text())='Groceries']") #Groceries title
