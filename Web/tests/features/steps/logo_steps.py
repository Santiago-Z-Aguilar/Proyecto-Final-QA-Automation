from behave import given, when, then
from Web.pages.home_page import HomePage
from selenium.common.exceptions import NoSuchElementException


@given("I am on the home page")
def step_impl(context):
    context.home = HomePage(context.driver)
    context.home.load()
    context.home.wait_for_header()


@when("I navigate to the Books category")
def step_impl(context):
    context.home.click_categories()
    context.home.go_to_books()
    context.current_url_before = context.driver.current_url
    context.home.wait_overlay_disappear()


@when("I click on the logo")
def step_impl(context):
    context.home.click_logo()
    context.current_url_after = context.driver.current_url


@then("I should be redirected back to the home page")
def step_impl(context):
    assert context.current_url_before == context.current_url_after, \
        f"Expected to be back at home, but got {context.current_url_after}"


@then("the logo should be visible on the page")
def step_impl(context):
    assert context.home.is_logo_displayed(), "The logo is not visible on the page."


@then("the logo should not be visible on the page")
def step_impl(context):
    if context.home.is_logo_displayed():
        raise AssertionError("The logo is present on the page, but it shouldn't be.")