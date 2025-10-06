# Web/tests/conftest.py

import pytest
from Web.pages.checkout_page import CheckoutPage


@pytest.fixture
def checkout_page(driver):
    """Fixture that provides a pre-loaded checkout page.
    Uses the existing driver fixture to create and initialize
    a checkout page with 2 products in the cart.
    """
    page = CheckoutPage(driver)
    page.load()
    return page