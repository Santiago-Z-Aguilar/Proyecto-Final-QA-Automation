# Web/tests/home/conftest.py

from Web.pages.home_page import HomePage
import pytest

@pytest.fixture
def home_page(driver):
    """Load home page"""
    home = HomePage(driver)
    home.load()
    return home