# Web/tests/shopping_cart/test_shopping_cart.py

from Web.locators.shopping_cart_locators import ShoppingCartLocators
from Web.test_data.products import *
from Web.tests.shopping_cart.conftest import cart_page, base_page, pdp_page, home_page, _round_2, add_from_pdp
from Web.utils.config import Config


# === Add from PDP ===
class TestAddFromPDP:
    def test_add_product_shows_in_cart(self, pdp_page, cart_page):
        name = add_from_pdp(pdp_page, ART_HISTORY, qty=1)
        cart_page.load()

        url = cart_page.driver.current_url

        assert cart_page.product_title_displayed(name), (
            f"Cart title not visible for '{name}'. "
            f"URL={url} Locator={ShoppingCartLocators.product_title(name)}"
        )

        assert cart_page.product_image_displayed(name), (
            f"Cart image not visible for '{name}'. "
            f"URL={url} Locator={ShoppingCartLocators.product_image_contains(name)}"
        )

        qty = cart_page.get_quantity()
        assert qty == 1, f"Quantity mismatch. expected=1 got={qty} URL={url}"

        unit = cart_page.get_product_price_value()
        subtotal = cart_page.get_summary_dict()["subtotal"]
        expected = _round_2(unit * 1)
        observed = _round_2(subtotal)
        assert observed == expected, (
            f"Subtotal mismatch. expected={expected:.2f} got={observed:.2f} "
            f"(unit={unit:.2f} qty=1) URL={url}"
        )


# === Quantity changes ===
class TestQuantityChanges:
    def test_increase_updates_subtotal(self, pdp_page, cart_page):
        add_from_pdp(pdp_page, ART_HISTORY, qty=1)
        cart_page.load()

        url = cart_page.driver.current_url
        new_qty = cart_page.click_increase_quantity(1)

        unit = cart_page.get_product_price_value()
        subtotal = cart_page.get_summary_dict()["subtotal"]
        observed = _round_2(subtotal)
        expected = _round_2(unit * new_qty)

        assert new_qty == 2, f"Quantity after '+' incorrect. expected=2 got={new_qty} URL={url}"
        assert observed == expected, (
            f"Subtotal after '+' incorrect. expected={expected:.2f} got={observed:.2f} "
            f"(unit={unit:.2f} qty={new_qty}) URL={url}"
        )

    def test_decrease_updates_subtotal(self, pdp_page, cart_page):
        name = ART_HISTORY
        add_from_pdp(pdp_page, name, qty=1)
        cart_page.load()

        url = cart_page.driver.current_url
        cart_page.click_increase_quantity(3)
        before_qty = cart_page.get_quantity()

        new_qty = cart_page.click_decrease_quantity(2)

        unit = cart_page.get_product_price_value()
        subtotal = cart_page.get_summary_dict()["subtotal"]
        observed = _round_2(subtotal)
        expected = _round_2(unit * new_qty)

        assert cart_page.product_title_displayed(name), f"Product row not visible for '{name}'. URL={url}"
        assert before_qty == 4, f"Unexpected pre-condition qty. expected=4 got={before_qty} URL={url}"
        assert new_qty == 2, f"Quantity after '-' incorrect. expected=2 got={new_qty} URL={url}"
        assert observed == expected, (
            f"Subtotal after '-' incorrect. expected={expected:.2f} got={observed:.2f} "
            f"(unit={unit:.2f} qty={new_qty}) URL={url}"
        )


# === Removing products ===
class TestRemoveProducts:
    def test_remove_only_item_makes_cart_empty(self, pdp_page, cart_page):
        add_from_pdp(pdp_page, ART_HISTORY, qty=1)
        cart_page.load()
        cart_page.remove_item()

        url = cart_page.driver.current_url
        assert cart_page.empty_title_visible(), f"Empty title not visible. URL={url}"
        assert cart_page.empty_desc_visible(), f"Empty description not visible. URL={url}"
        assert cart_page.element_is_visible(ShoppingCartLocators.CONTINUE_SHOPPING_BTN), (
            f"'Continue Shopping' not visible. URL={url} "
            f"Locator={ShoppingCartLocators.CONTINUE_SHOPPING_BTN}"
        )

    def test_remove_one_item_keeps_other_visible(self, pdp_page, cart_page):
        add_from_pdp(pdp_page, ART_HISTORY, qty=1)
        add_from_pdp(pdp_page, DENIM_JEANS, qty=1)
        cart_page.load()

        cart_page.remove_item()
        cart_page.load()

        url = cart_page.driver.current_url
        assert (
                cart_page.product_title_displayed(DENIM_JEANS)
                or cart_page.product_title_displayed(ART_HISTORY)
        ), (
            f"No items visible after removing one. expected one of "
            f"['{DENIM_JEANS}', '{ART_HISTORY}'] to remain. URL={url}"
        )


# === Order summary math ===
class TestOrderSummary:
    def test_summary_changes_when_quantity_changes(self, pdp_page, cart_page):
        add_from_pdp(pdp_page, ART_HISTORY, qty=1)
        cart_page.load()

        before = _round_2(cart_page.get_summary_dict()["subtotal"])
        cart_page.click_increase_quantity(2)
        after = _round_2(cart_page.get_summary_dict()["subtotal"])

        assert after != before, f"Subtotal did not change. before={before:.2f} after={after:.2f}"

    def test_subtotal_equals_unit_times_qty(self, pdp_page, cart_page):
        add_from_pdp(pdp_page, ART_HISTORY, qty=3)
        cart_page.load()

        unit = cart_page.get_product_price_value()
        qty = cart_page.get_quantity()
        observed = _round_2(cart_page.get_summary_dict()["subtotal"])
        expected = _round_2(unit * qty)

        assert observed == expected, (
            f"Subtotal != unit*qty. expected={expected:.2f} got={observed:.2f} "
            f"(unit={unit:.2f} qty={qty})"
        )

    def test_shipping_is_free_above_threshold(self, pdp_page, cart_page):
        add_from_pdp(pdp_page, ART_HISTORY, qty=3)
        cart_page.load()

        s = cart_page.get_summary_dict()
        ship = _round_2(s["shipping"])
        sub = _round_2(s["subtotal"])
        assert ship == 0.0, f"Shipping not free over threshold. subtotal={sub:.2f} shipping={ship:.2f}"

    def test_shipping_is_non_negative(self, pdp_page, cart_page):
        add_from_pdp(pdp_page, ART_HISTORY, qty=1)
        cart_page.load()

        ship = cart_page.get_summary_dict()["shipping"]
        assert ship >= 0.0, f"Invalid shipping value. shipping={ship}"

    def test_tax_is_taxrate_of_subtotal(self, pdp_page, cart_page):
        add_from_pdp(pdp_page, ART_HISTORY, qty=3)
        cart_page.load()

        s = cart_page.get_summary_dict()
        expected = _round_2(s["subtotal"] * TAX_RATE)
        observed = _round_2(s["tax"])
        assert observed == expected, (
            f"Tax mismatch. expected={expected:.2f} got={observed:.2f} "
            f"(subtotal={_round_2(s['subtotal']):.2f} tax_rate={TAX_RATE})"
        )

    def test_total_equals_subtotal_plus_shipping_plus_tax(self, pdp_page, cart_page):
        add_from_pdp(pdp_page, ART_HISTORY, qty=3)
        cart_page.load()

        s = cart_page.get_summary_dict()
        expected = _round_2(s["subtotal"] + s["shipping"] + s["tax"])
        observed = _round_2(s["total"])
        assert observed == expected, (
            f"Total mismatch. expected={expected:.2f} got={observed:.2f} "
            f"(subtotal={_round_2(s['subtotal']):.2f} shipping={_round_2(s['shipping']):.2f} tax={_round_2(s['tax']):.2f})"
        )


# === Cart navigation ===
class TestCartNavigation:
    def test_proceed_to_checkout_redirects(self, pdp_page, cart_page, base_page):
        add_from_pdp(pdp_page, ART_HISTORY, qty=1)
        cart_page.load()

        before = cart_page.driver.current_url
        cart_page.click_proceed_to_checkout()

        base_page.wait_for_url_contains("/checkout")

        url = cart_page.driver.current_url
        assert "/checkout" in url.lower(), f"Did not reach checkout. before={before} now={url}"

    def test_continue_shopping_redirects(self, pdp_page, cart_page, base_page, home_page):
        add_from_pdp(pdp_page, ART_HISTORY, qty=1)
        cart_page.load()

        before = cart_page.driver.current_url
        cart_page.click_continue_shopping()

        home_page.shop_by_category_displayed()
        url = cart_page.driver.current_url
        assert f"{Config.CART}" not in url.lower(), f"Still on cart after 'Continue Shopping'. before={before} now={url}"

# === Empty cart state ===
class TestEmptyCartState:
    def test_empty_cart_messages_visible(self, cart_page):
        cart_page.load()
        url = cart_page.driver.current_url

        assert cart_page.empty_title_visible(), (
            f"Empty title not visible. URL={url} Locator={ShoppingCartLocators.EMPTY_TITLE}"
        )
        assert cart_page.empty_desc_visible(), (
            f"Empty description not visible. URL={url} Locator={ShoppingCartLocators.EMPTY_DESC}"
        )
        assert cart_page.element_is_visible(ShoppingCartLocators.EMPTY_CONTINUE_SHOPPING_BTN), (
            f"'Continue Shopping' not visible on empty cart. URL={url} "
            f"Locator={ShoppingCartLocators.EMPTY_CONTINUE_SHOPPING_BTN}"
        )

    def test_empty_cart_continue_shopping_redirects(self, cart_page):
        cart_page.load()
        cart_page.click_empty_continue_shopping()

        url = cart_page.driver.current_url
        assert (
            (Config.BASE_URL in url) or (Config.PRODUCT_DETAIL in url)
        ), f"Unexpected redirect from empty cart CTA. url={url} expected_contains=[BASE_URL, PRODUCT_DETAIL]"
