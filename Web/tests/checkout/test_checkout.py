
from Web.locators.checkout_locators import CheckoutLocators
from Web.test_data.test_data import USER_CHECKOUT_FIELDS,VALID_USER_CHECKOUT,INCOMPLETE_EMAIL_USERS
import pytest

class TestCheckout:

    def test_validate_checkout(self,checkout_page):
        checkout_page.fill_form(VALID_USER_CHECKOUT)
        checkout_page.place_order()
        assert checkout_page.confirmation_page_loaded(),(
            f"{CheckoutLocators.PURCHASE_CONFIRMATION} label not displayed."
            f"URL {checkout_page.driver.current_url}"
            f"Locator: {CheckoutLocators.PURCHASE_CONFIRMATION}"
        )

    @pytest.mark.parametrize("skipped_field", USER_CHECKOUT_FIELDS)
    def test_checkout_missing_required_element(self,skipped_field,checkout_page):
        checkout_page.fill_form(VALID_USER_CHECKOUT,skipped_field)
        checkout_page.place_order()
        assert checkout_page.get_alert_text() == "Please fill in all required fields",(
            "Alert message not displayed."
            f"URL: {checkout_page.driver.current_url}")

    @pytest.mark.parametrize("user",INCOMPLETE_EMAIL_USERS)
    def test_email_format(self,user,checkout_page):
        checkout_page.fill_form(user)
        checkout_page.place_order()
        assert checkout_page.get_validation_message() is not None,(
            'Alert message not displayed.'
            f"URL: {checkout_page.driver.current_url}"
        )


    def test_phone_format(self):

        return

    def test_validate_order_summary(self):
        return

    def test_validate_total_price(self):
        return





