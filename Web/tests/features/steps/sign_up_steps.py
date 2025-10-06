from behave import given, when, then
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Web.pages.signup_page import SignUpPage
from Web.locators.header_locators import HeaderLocators
from Web.utils.config import Config


# --- GIVEN ---
@given("I am on the Home page")
def step_impl(context):
    context.driver.get(Config.BASE_URL)


@given("I am on the Sign Up page")
def step_impl(context):
    context.driver.get(Config.BASE_URL + "/signup")
    context.sign_up_page = SignUpPage(context.driver)


# --- WHEN ---
@when("I click the Sign Up button")
def step_impl(context):
    button = context.driver.find_element(*HeaderLocators.HEADER_SIGNUP)
    button.click()
    context.clicked_signup = True


@when(
    'I submit the form with firstname "{firstname}", lastname "{lastname}", email "{email}", zipcode "{zipcode}", password "{password}"'
)
def step_impl(context, firstname, lastname, email, zipcode, password):
    context.sign_up_page.sign_up_as_new_user(
        firstname, lastname, email, zipcode, password
    )

# --- THEN ---
@then('I must be redirected to "{path}"')
def step_impl(context, path):
    WebDriverWait(context.driver, 10).until(EC.url_contains(path))
    assert path in context.driver.current_url, f"Expected {path}, got {context.driver.current_url}"


@then("the Sign Up button should be visible on the page")
def step_impl(context):
    WebDriverWait(context.driver, 20).until(
        EC.visibility_of_element_located(HeaderLocators.HEADER_SIGNUP)
    )
    button = context.driver.find_element(*HeaderLocators.HEADER_SIGNUP)
    assert button.is_displayed(), "Sign Up button is not visible."


@then('I will not be redirected to "{path}"')
def step_impl(context, path):
    assert path not in context.driver.current_url, f"Unexpected redirect to {path}"


@then('the sign up should be "{result}"')
def step_impl(context, result):
    if result == "success":
        context.sign_up_page.assert_successful_sign_up()
    elif result == "failure":
        context.sign_up_page.assert_unsuccessful_sign_up()
    else:
        raise AssertionError(f"Unexpected result value: {result}")