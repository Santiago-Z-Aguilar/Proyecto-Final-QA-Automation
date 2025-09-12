# Web/locators/home_locators.py

from selenium.webdriver.common.by import By

class HomeLocators:

    LABEL_SHOP_BY_CATEGORY = (By.XPATH, "//h2[text()='Shop by Category']")

    SHOP_BY_CATEGORY = (By.XPATH, "//h2[contains(normalize-space(),'Shop by Category')]")

    # ---------- CATEGORIES ----------
    MENS_CLOTHES = (By.XPATH, "//a[normalize-space()=\"Men's Clothes\"]")
    WOMEN_CLOTHES = (By.XPATH, "//a[normalize-space()=\"Women's Clothes\"]")
    ELECTRONICS = (By.XPATH, "//a[normalize-space()='Electronics']")
    BOOKS = (By.XPATH, "//a[normalize-space()='Books']")
    GROCERIES = (By.XPATH, "//a[normalize-space()='Groceries']")

    # ---------- SPECIAL DEALS ----------
    SPECIAL_DEALS_TITLE = (By.XPATH, "//h2[contains(text(), 'Special Deals')]")
    VIEW_ALL_DEALS_BUTTON = (By.XPATH, "//button[contains(text(), 'View All Deals')]")


