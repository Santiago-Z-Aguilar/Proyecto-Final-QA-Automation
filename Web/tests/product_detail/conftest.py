# Web/tests/conftest.py
import pytest

from Web.conftest import driver_class
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

@pytest.fixture
def product_page_class(driver_class):
    """Fixture that provides a pre-loaded product detail page.
    Uses the existing driver fixture to create and initialize
    a ProductDetailPage instance with default product ID.
    Scope: Class.
    """
    page = ProductDetailPage(driver=driver_class)
    page.load(product_id=31)  # Default test product ID
    return page