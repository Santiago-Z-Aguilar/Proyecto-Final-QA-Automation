
from Web.locators.checkout_locators import CheckoutLocators
from Web.test_data.test_data import USER_CHECKOUT_FIELDS
import pytest

class TestCheckout:

    def test_validate_checkout(self,checkout_page):
        checkout_page.load()
        checkout_page.fill_form()
        checkout_page.place_order()
        assert checkout_page.confirmation_page_loaded(),(
            f"{CheckoutLocators.PURCHASE_CONFIRMATION} label not displayed."
            f"URL {checkout_page.driver.current_url}"
            f"Locator: {CheckoutLocators.PURCHASE_CONFIRMATION}"
        )

    @pytest.mark.parametrize("skipped_field", USER_CHECKOUT_FIELDS)
    def test_checkout_missing_required_element(self,skipped_field,checkout_page):
        checkout_page.load()
        checkout_page.fill_form(skipped_field)
        checkout_page.place_order()
        assert checkout_page.get_alert_text() == "Please fill in all required fields"

    def test_email_format(self):
        return

    def test_phone_format(self):
        return

    def test_validate_order_summary(self):
        return

    def test_validate_total_price(self):
        return





