# Web/tests/logo/test_logo.py

import pytest
from Web.pages.home_page import HomePage


def test_logo_redirects_home(driver):
    home = HomePage(driver)
    home.load()
    home.wait_for_header()

    # Navigate to Books
    home.click_categories()
    home.go_to_books()
    current_url_before = driver.current_url

    # Wait for overlay to disappear
    home.wait_overlay_disappear()

    # Click on logo
    home.click_logo()
    current_url_after = driver.current_url

    assert current_url_before == current_url_after, f"The logo redirects to the home page"


def test_logo_displayed(driver):
    home = HomePage(driver)
    home.load()
    home.wait_for_header()

    assert home.is_logo_displayed(), "The logo is visible on the page."


def test_logo_not_displayed_negative(driver):
    home = HomePage(driver)
    home.load()
    home.wait_for_header()

    # This test is designed to be negative (it will only fail if the logo is present).
    if home.is_logo_displayed():
        pytest.fail("The logo is present on the page, but it shouldn't be.")