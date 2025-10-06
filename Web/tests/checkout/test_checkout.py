
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

    def test_validate_product_prices(self,checkout_page):
        assert checkout_page.is_product_price_displayed(),(
            "Product prices not displayed."
            f"URL: {checkout_page.driver.current_url}"
        )

    def test_validate_subtotal(self,checkout_page):
        assert checkout_page.is_subtotal_displayed(),(
            "Subtotal not displayed."
            f"URL: {checkout_page.driver.current_url}"
            f"Locator: {CheckoutLocators.SUBTOTAL_ROW}"
        )

    def test_validate_shipping(self, checkout_page):
        assert checkout_page.is_shipping_displayed(),(
            "Subtotal not displayed."
            f"URL: {checkout_page.driver.current_url}"
            f"Locator: {CheckoutLocators.SHIPPING_ROW}"
        )

    def test_validate_tax(self, checkout_page):
        assert checkout_page.is_tax_displayed(),(
            "Subtotal not displayed."
            f"URL: {checkout_page.driver.current_url}"
            f"Locator: {CheckoutLocators.TAX_ROW}"
        )

    def test_validate_subtotal_price(self,checkout_page):
        assert checkout_page.subtotal_calculation() == checkout_page.get_subtotal_price(),(
            "Subtotal price doesnt match "
        )

    def test_validate_total_price(self,checkout_page):
        assert checkout_page.total_calculation() == checkout_page.get_total_price(),(
            "Total price doesnt match "
        )







