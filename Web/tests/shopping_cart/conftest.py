# Web/tests/shopping_cart/conftest.py

import pytest

from Web.pages.base_page import BasePage
from Web.pages.home_page import HomePage
from Web.pages.product_detail_page import ProductDetailPage
from Web.pages.shopping_cart_page import ShoppingCartPage
from Web.test_data.products import PRODUCTS

# === Fixtures ===
@pytest.fixture
def cart_page(driver):
    page = ShoppingCartPage(driver)
    page.load()
    return page


@pytest.fixture
def base_page(driver):
    return BasePage(driver)


@pytest.fixture
def pdp_page(driver):
    return ProductDetailPage(driver)


@pytest.fixture
def home_page(driver):
    return HomePage(driver)

# === Helpers ===
def _round_2(x):
    return round(x + 1e-9, 2)


def add_from_pdp(pdp_page, product_key, qty=1):
    """Load PDP by product_id and add qty units to cart."""
    pid = PRODUCTS[product_key]["id"]
    pdp_page.load(product_id=pid)
    for _ in range(qty):
        pdp_page.click_add_to_cart()
    return product_key
