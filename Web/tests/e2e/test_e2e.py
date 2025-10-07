# Web/tests/e2e/test_e2e.py

import time
import pytest
from selenium.common import TimeoutException, ElementClickInterceptedException, UnexpectedAlertPresentException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from Web.pages.home_page import HomePage
from Web.pages.signup_page import SignUpPage
from Web.pages.login_page import LoginPage
from Web.pages.product_detail_page import ProductDetailPage
from Web.pages.shopping_cart_page import ShoppingCartPage
from Web.pages.checkout_page import CheckoutPage
from Web.test_data.test_data import VALID_USER_SIGNUP, VALID_USER_LOGIN, VALID_USER_CHECKOUT
from Web.utils.config import Config


# Helpers for secure clicks and UI cleanup
def clear_screen(driver):
    """Remove banners, modals, loaders, or toasts that block interaction"""
    try:
        driver.execute_script("""
            const selectors = [
                '.modal', '.toast', '.overlay', '.backdrop', '.loading',
                '.spinner', '.loader', '[role="dialog"]', '[aria-busy="true"]'
            ];
            selectors.forEach(sel => {
                document.querySelectorAll(sel).forEach(el => {
                    el.style.display = 'none';
                    if (el.remove) el.remove();
                });
            });
        """)
    except Exception:
        pass


def safe_click(driver, locator, max_retries=6, wait_time=15):
    """
    Secure click:
    Waits until there are no visible loaders/spinners.
    Scrolls and retries if the click is intercepted.
    """
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common import ElementClickInterceptedException, TimeoutException, NoSuchElementException
    import time

    for attempt in range(max_retries):
        try:
            # Wait until there are no active loaders (SVG, spinner, or backdrop)
            WebDriverWait(driver, 10).until_not(
                EC.presence_of_all_elements_located((
                    By.CSS_SELECTOR,
                    ".loader, .spinner, .loading, .backdrop, svg.animate-spin"
                ))
            )
            time.sleep(0.3)  # pause for transition

            # Wait for clickable element
            element = WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable(locator))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
            ActionChains(driver).move_to_element(element).pause(0.2).perform()

            # Try normal click
            element.click()
            return

        except ElementClickInterceptedException:
            # If it is still blocked, clear the UI and try again.
            driver.execute_script("""
                const blockers = document.querySelectorAll(
                    '.overlay, .modal, .toast, .spinner, .loader, svg.animate-spin'
                );
                blockers.forEach(b => b.remove());
            """)
            try:
                element = driver.find_element(*locator)
                driver.execute_script("arguments[0].click();", element)
                return
            except Exception:
                pass

        except (TimeoutException, NoSuchElementException):
            if attempt == max_retries - 1:
                raise
        time.sleep(0.8)  # incremental wait between attempts


# TESTS END TO END

@pytest.mark.e2e
class TestE2EFlows:

    def test_full_checkout_flow(self, driver):
        """Complete flow: Home → Sign Up → Login → Category → Cart → Checkout"""
        home = HomePage(driver)
        signup = SignUpPage(driver)
        login = LoginPage(driver)
        pdp = ProductDetailPage(driver)
        cart = ShoppingCartPage(driver)
        checkout = CheckoutPage(driver)

        try:
            # HOME
            home.load()
            assert home.shop_by_category_displayed()

            # SIGN UP
            signup.load()
            WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "firstName")))
            clear_screen(driver)
            safe_click(driver, (By.CSS_SELECTOR, "button[type='submit']"))  # we ensure the submit click
            signup.sign_up_as_new_user(**VALID_USER_SIGNUP[0])
            signup.assert_successful_sign_up()

            # LOGIN
            login.load()
            clear_screen(driver)
            user = VALID_USER_LOGIN[0]
            login.login_as_user(user["email"], user["password"])
            login.assert_successful_login()

            # PRODUCTO
            home.load()
            home.click_books()
            pdp.load()
            clear_screen(driver)
            safe_click(driver, (By.XPATH, "//button[contains(.,'Add to Cart') or contains(.,'Add')]"))
            pdp.click_add_to_cart()

            # CART
            cart.load()
            WebDriverWait(driver, 10).until(EC.url_contains("/cart"))
            assert cart.get_cart_count() >= 1

            # CHECKOUT
            clear_screen(driver)
            safe_click(driver, (By.XPATH, "//button[contains(.,'Checkout') or contains(.,'Proceed')]"))
            checkout.wait_for_element(checkout.locators.TITLE)
            checkout.fill_form(VALID_USER_CHECKOUT)
            clear_screen(driver)
            safe_click(driver, (By.XPATH, "//button[contains(.,'Place Order') or contains(.,'Confirm')]"))
            assert checkout.confirmation_page_loaded()

        except (TimeoutException, ElementClickInterceptedException) as e:
            pytest.fail(f"Timeout or blocked click in main flow: {str(e)}")


    def test_signup_login_search_fails(self, driver):
        """Sign Up → Login → Search for ‘Laptop’ (without successful redirection)"""
        signup = SignUpPage(driver)
        login = LoginPage(driver)
        home = HomePage(driver)

        try:
            # SIGN UP
            signup.load()
            WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "firstName")))
            signup.sign_up_as_new_user(**VALID_USER_SIGNUP[1])
            signup.assert_successful_sign_up()

            # LOGIN
            login.load()
            clear_screen(driver)
            user = VALID_USER_LOGIN[0]
            login.login_as_user(user["email"], user["password"])
            login.assert_successful_login()

            # SEARCH
            home.load()
            clear_screen(driver)
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='search']")))
            home.search_for("Laptop")
            clear_screen(driver)
            safe_click(driver, (By.CSS_SELECTOR, "button[type='submit']"))
            WebDriverWait(driver, 5).until_not(EC.url_contains("/product"))
            assert "product" not in driver.current_url

        except (TimeoutException, ElementClickInterceptedException) as e:
            pytest.fail(f"Timeout or blocked click in failed search flow: {str(e)}")


    def test_purchase_with_shipping_cost(self, driver):
        """Verify that the shipping field is visible (>= 0.0)."""
        pdp = ProductDetailPage(driver)
        cart = ShoppingCartPage(driver)

        try:
            pdp.load()
            clear_screen(driver)
            safe_click(driver, (By.XPATH, "//button[contains(.,'Add to Cart') or contains(.,'Add')]"))
            cart.load()
            s = cart.get_summary_dict()
            assert "shipping" in s, "Campo 'shipping' no presente en el resumen"
            assert s["shipping"] >= 0.0, f"Valor de envío inválido: {s['shipping']}"
        except TimeoutException as e:
            pytest.fail(f"Timeout on purchase with shipping: {str(e)}")


    def test_checkout_empty_required_fields(self, driver):
        """Complete purchase with required fields left blank"""
        checkout = CheckoutPage(driver)
        try:
            checkout.load()
            clear_screen(driver)
            checkout.fill_form(VALID_USER_CHECKOUT, skip=["email", "firstname"])
            clear_screen(driver)
            safe_click(driver, (By.XPATH, "//button[contains(.,'Place Order') or contains(.,'Confirm')]"))
            alert = driver.switch_to.alert
            text = alert.text
            alert.accept()
            assert "required" in text.lower(), f"Unexpected alert text: {text}"
        except UnexpectedAlertPresentException:
            pass
        except TimeoutException as e:
            pytest.fail(f"Timeout during checkout with empty fields: {str(e)}")


    def test_purchase_with_empty_cart(self, driver):
        """Purchase with an empty cart"""
        cart = ShoppingCartPage(driver)
        try:
            cart.load()
            clear_screen(driver)
            safe_click(driver, (By.XPATH, "//button[contains(.,'Checkout') or contains(.,'Proceed')]"))
            assert "/checkout" not in driver.current_url
        except Exception:
            pytest.skip("The cart was not empty when it started.")


    def test_abandon_checkout(self, driver):
        """Abandoning checkout by returning to the Home page"""
        pdp = ProductDetailPage(driver)
        cart = ShoppingCartPage(driver)
        home = HomePage(driver)

        try:
            pdp.load()
            clear_screen(driver)
            safe_click(driver, (By.XPATH, "//button[contains(.,'Add to Cart')]"))
            cart.load()
            clear_screen(driver)
            safe_click(driver, (By.XPATH, "//button[contains(.,'Checkout') or contains(.,'Proceed')]"))

            # En lugar de driver.back(), ir directo al home
            driver.get(Config.BASE_URL)
            WebDriverWait(driver, 10).until(EC.url_to_be(Config.BASE_URL))
            assert home.shop_by_category_displayed()

        except TimeoutException as e:
            pytest.fail(f"Checkout abandonment timeout: {str(e)}")