# Web/tests/conftest.py
import pytest
from Web.pages.product_detail_page import ProductDetailPage


@pytest.fixture
def product_page(driver):
    """Fixture that provides a pre-loaded product detail page.
    Uses the existing driver fixture to create and initialize
    a ProductDetailPage instance with default product ID.
    """
    page = ProductDetailPage(driver)
    page.load(product_id=31)  # Default test product ID
    return page

