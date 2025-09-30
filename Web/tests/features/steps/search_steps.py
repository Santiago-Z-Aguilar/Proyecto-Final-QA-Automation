import os, time
from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from Web.pages.home_page import HomePage


def save_screenshot(driver, name):
    os.makedirs("screenshots", exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    path = os.path.join("screenshots", f"{name}_{timestamp}.png")
    driver.save_screenshot(path)
    print(f"\n📸 Saved in: {path}")



@when('I search for "{product}"')
def step_impl(context, product):
    search_input = context.driver.find_element(By.CSS_SELECTOR, "input[placeholder='Search products...']")
    search_input.send_keys(product)
    search_input.send_keys(Keys.ENTER)
    context.expected_url = "https://shophub-commerce.vercel.app/product/22"


@then('I should not be redirected to "{url}"')
def step_impl(context, url):
    try:
        WebDriverWait(context.driver, 5).until(lambda d: d.current_url == url)
    except Exception:
        # ✅ Correct: we expected it NOT to redirect
        assert context.driver.current_url != url, \
            f"Unexpected redirection to {url}"
        return

    #
    # If it redirected, this is a fail
    raise AssertionError(f"Redirected to {url}, but it should not have.")


@then('a screenshot is taken with name "{screenshot_name}"')
def step_impl(context, screenshot_name):
    save_screenshot(context.driver, screenshot_name)