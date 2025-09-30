from behave import given, when, then
from Web.pages.home_page import HomePage
from Web.pages.banner_slider_page import BannerSliderPage
from selenium.webdriver.support.ui import WebDriverWait


@given("I am on the home page with the banner slider")
def step_impl(context):
    context.driver.get("https://shophub-commerce.vercel.app/")
    context.slider = BannerSliderPage(context.driver)

# --- Navigation with arrows ---

@when("I click the next arrow")
def step_impl(context):
    context.slider.click_next()

@when("I click the previous arrow")
def step_impl(context):
    context.slider.click_prev()

@when('I click the next arrow again')
def step_impl(context):
    # Si ya existe en context, usarlo; si no, crearlo
    if not hasattr(context, "slider"):
        context.slider = BannerSliderPage(context.driver)
    context.slider.click_next()

@then("the slide should change")
def step_impl(context):
    current_src = context.slider.get_active_slide_src()
    assert hasattr(context, "last_src") is False or context.last_src != current_src, \
        f"Slide did not change (still {current_src})"
    context.last_src = current_src

@then("another slide should be displayed")
def step_impl(context):
    new_src = context.slider.get_active_slide_src()
    assert new_src != context.last_src, f"Expected a different slide, got same src {new_src}"
    context.last_src = new_src

@then("the slider should return to the previous slide")
def step_impl(context):
    back_src = context.slider.get_active_slide_src()
    assert back_src == context.last_src, f"Did not return to previous slide (expected {context.last_src}, got {back_src})"


# --- Navigation with dots ---

@then("the first dot should be active")
def step_impl(context):
    active_index = context.slider.get_active_dot_index()
    assert active_index == 0, f"Expected dot 0 active, got {active_index}"

@when("I click on the second dot")
def step_impl(context):
    context.slider.click_dot(1)

@then("the second dot should be active")
def step_impl(context):
    active_index = context.slider.get_active_dot_index()
    assert active_index == 1, f"Expected dot 1 active, got {active_index}"

@when("I click on the third dot")
def step_impl(context):
    context.slider.click_dot(2)

@then("the third dot should be active")
def step_impl(context):
    active_index = context.slider.get_active_dot_index()
    assert active_index == 2, f"Expected dot 2 active, got {active_index}"


# --- Buttons redirect ---

@when('I click the "Shop Now" button on the first slide')
def step_impl(context):
    btn = context.slider.get_active_slide_button()
    assert btn.text.strip() == "Shop Now"
    context.slider.driver.execute_script("arguments[0].click();", btn)

@then('I will be redirected to the "men-clothes" category')
def step_impl(context):
    expected_url = "https://shophub-commerce.vercel.app/categories/men-clothes"
    WebDriverWait(context.driver, 10).until(lambda d: d.current_url == expected_url)
    assert context.driver.current_url == expected_url

@when('I move to the second slide')
def step_impl(context):
    context.slider.click_next()

@when('I click the "Explore" button')
def step_impl(context):
    btn = context.slider.get_active_slide_button()
    assert btn.text.strip() == "Explore"
    context.slider.driver.execute_script("arguments[0].click();", btn)

@then('I should be redirected to the "electronics" category')
def step_impl(context):
    expected_url = "https://shophub-commerce.vercel.app/categories/electronics"
    WebDriverWait(context.driver, 10).until(lambda d: d.current_url == expected_url)
    assert context.driver.current_url == expected_url

@when('I move to the third slide')
def step_impl(context):
    context.slider.click_next()
    context.slider.click_next()

@when('I click the "Order Now" button')
def step_impl(context):
    btn = context.slider.get_active_slide_button()
    assert btn.text.strip() == "Order Now"
    context.slider.driver.execute_script("arguments[0].click();", btn)

@then('I should be redirected to the "groceries" category')
def step_impl(context):
    expected_url = "https://shophub-commerce.vercel.app/categories/groceries"
    WebDriverWait(context.driver, 10).until(lambda d: d.current_url == expected_url)
    assert context.driver.current_url == expected_url