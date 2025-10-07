from .base_page import BasePage
from Web.locators.plp_locators import PlpLocators
from Web.utils.config import Config
import os
from datetime import datetime
import time
from selenium.common.exceptions import (
        TimeoutException,
    )
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Web.locators.header_locators import HeaderLocators
import random
from selenium.webdriver.common.by import By
from Web.locators.shopping_cart_locators import ShoppingCartLocators
from Web.utils.data import CATEGORY_SLUGS


class PlpPage(BasePage, Config):

    def load_home(self):
        self.visit(self.BASE_URL)

    # --- Esperar carga completa ---
    def wait_for_page_load1(self, timeout=15):
        WebDriverWait(self.driver, timeout).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

    def go_to_category(self, category_name: str):
        locator = PlpLocators.category_locator(category_name)
        WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(locator))
        self.click(locator)
        WebDriverWait(self.driver, 15).until(EC.invisibility_of_element_located(PlpLocators.SPINNER))
####hassta aqui quede
    # --- Validaciones ---
    def assert_category_title(self, category_name: str):
        locator = PlpLocators.category_title_locator(category_name)
        element = WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(locator))
        assert element.is_displayed(), f"El título de la categoría '{category_name}' no se muestra en pantalla"
        assert element.text.strip() == category_name, f"El título esperado '{category_name}' no coincide con '{element.text.strip()}'"

    def assert_category_description(self, expected_text: str):
        locator = PlpLocators.category_description()
        element = WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(locator))
        assert element.is_displayed(), "La descripción de la categoría no se muestra"
        assert element.text.strip() == expected_text, f"Se esperaba '{expected_text}' pero se encontró '{element.text.strip()}'"

    def assert_products_display(self, category_name: str, test_name: str):
        WebDriverWait(self.driver, 15).until(EC.visibility_of_all_elements_located(PlpLocators.PRODUCT_CARD))
        products = self.driver.find_elements(*PlpLocators.PRODUCT_CARD)
        assert len(products) > 0, "No se encontraron productos en la PLP"

        # Screenshot antes de scroll
        self.take_screenshot(test_name, category_name, suffix="before_scroll")

        for index, product in enumerate(products, start=1):
            print(f"\nRevisando producto {index}...")

            name = product.find_element(*PlpLocators.PRODUCT_NAME).text.strip()
            price = product.find_element(*PlpLocators.PRODUCT_PRICE).text.strip()
            image = product.find_element(*PlpLocators.PRODUCT_IMAGE)
            desc = product.find_element(*PlpLocators.PRODUCT_DESC)
            view_btn = product.find_element(*PlpLocators.VIEW_DETAILS_BTN)
            add_btn = product.find_element(*PlpLocators.ADD_TO_CART_BTN)

            print(f"Nombre: '{name}'")
            assert name, f"[Producto {index}] El nombre está vacío"

            print(f"Descripción: '{desc.text.strip()}'")
            assert desc.is_displayed() and desc.text.strip(), f"[Producto {index}] La descripción está vacía"

            print(f"Precio: '{price}'")
            assert price.startswith("$"), f"[Producto {index}] El precio es inválido: {price}"

            print(f"Imagen visible: {image.is_displayed()}")
            assert image.is_displayed(), f"[Producto {index}] La imagen no se muestra"

            print(f"Botón 'View Details': {view_btn.is_displayed()}")
            assert view_btn.is_displayed(), f"[Producto {index}] El botón 'View Details' no se muestra"

            print(f"Botón 'Add to Cart': {add_btn.is_displayed()}")
            assert add_btn.is_displayed(), f"[Producto {index}] El botón 'Add to Cart' no se muestra"

            print(f"Producto {index} validado correctamente.\n")

        # Hacer scroll hasta el último producto
        last_product = products[-1]
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'end'});", last_product)
        time.sleep(1)

        # Screenshot después del scroll
        self.take_screenshot(test_name, category_name, suffix="after_scroll")

        # --- Validación de apertura de PDP ---

    def assert_first_product_opens_pdp(self, category_name: str, test_name: str):
        print(f"Abriendo PDP del primer producto en categoría: {category_name}")

        # Click al primer producto
        first_product = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(PlpLocators.first_product())
        )
        first_product.click()
        # Esperar a que el spinner desaparezca
        WebDriverWait(self.driver, 15).until(
            EC.invisibility_of_element_located(PlpLocators.SPINNER)
        )
        # Esperar botón "Add to Cart" en PDP
        add_to_cart_btn = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(PlpLocators.pdp_add_to_cart_btn())
        )
        # Screenshot de la PDP ya cargada
        self.take_screenshot(test_name, category_name, suffix="pdp")
        # Validación
        assert add_to_cart_btn.is_displayed(), (
            f"No se encontró el botón 'Add to Cart' en la PDP de {category_name}"
        )
        print(f"PDP validada correctamente para categoría: {category_name}")

# --- Productos ---
    def get_all_products(self):
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_all_elements_located(PlpLocators.PRODUCT_CARD)
        )
        products = self.driver.find_elements(*PlpLocators.PRODUCT_CARD)
        assert products, "No se encontraron productos en la PLP"
        return products
    def get_random_product(self):
        products = self.get_all_products()
        return random.choice(products)
    def open_cart(self):
        self.click(HeaderLocators.CART_ICON)

    # --- Metodo para agregar producto aleatorio al carrito ---
    def add_random_product_to_cart(self, category_name: str, test_name: str):
        try:
            WebDriverWait(self.driver, 15).until(EC.visibility_of_all_elements_located(PlpLocators.PRODUCT_CARD))
            products = self.driver.find_elements(*PlpLocators.PRODUCT_CARD)
            assert products, "No se encontraron productos en la PLP"
            product = random.choice(products)
            product_name = product.find_element(*PlpLocators.PRODUCT_NAME).text.strip()
            # Screenshot antes de clic
            self.take_screenshot(test_name, category_name, suffix=f"before_click_{product_name}")
            add_btn = product.find_element(*PlpLocators.ADD_TO_CART_BTN)
            add_btn.click()
            # Validar actualización del carrito
            cart_count_locator = HeaderLocators.CART_COUNT
            try:
                WebDriverWait(self.driver, 10).until(
                    lambda d: int(d.find_element(*cart_count_locator).text.strip()) > 0
                )
            except Exception:
                self.take_screenshot(test_name, category_name, suffix=f"cart_not_updated_{product_name}")
                raise AssertionError(f"El carrito no se actualizó al agregar el producto '{product_name}'")
            # Screenshot después de actualizar carrito
            self.take_screenshot(test_name, category_name, suffix=f"after_cart_update_{product_name}")
            return product_name
        except Exception as e:
            # Screenshot genérico en caso de error inesperado
            self.take_screenshot(test_name, category_name, suffix=f"error_add_to_cart")
            raise e

    def add_random_product_to_cart2(self, category_name: str, test_name: str):
        WebDriverWait(self.driver, 15).until(EC.visibility_of_all_elements_located(PlpLocators.PRODUCT_CARD))
        products = self.driver.find_elements(*PlpLocators.PRODUCT_CARD)
        assert products, "No se encontraron productos en la PLP"
        product = random.choice(products)
        product_name = product.find_element(*PlpLocators.PRODUCT_NAME).text.strip()
        # Screenshot antes de clic
        self.take_screenshot(test_name, category_name, suffix="before_click")
        add_btn = product.find_element(*PlpLocators.ADD_TO_CART_BTN)
        add_btn.click()
        # Esperar que el icono del carrito se actualice
        cart_count_locator = HeaderLocators.CART_COUNT
        WebDriverWait(self.driver, 10).until(
            lambda d: int(d.find_element(*cart_count_locator).text.strip()) > 0
        )
        # Screenshot después de actualizar carrito
        self.take_screenshot(test_name, category_name, suffix="after_cart_update")
        return product_name

    # --- Metodo para abrir carrito y esperar que cargue ---
    def open_cart_and_wait(self, test_name: str, timeout: int = 15):
        cart_button = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(HeaderLocators.CART_ICON)
        )
        # Scroll + JS click para evitar intercept
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", cart_button)
        self.driver.execute_script("arguments[0].click();", cart_button)
        # Esperar spinner desaparezca
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(PlpLocators.SPINNER)
            )
        except TimeoutException:
            print("Spinner no desapareció a tiempo, tomando screenshot de todos modos")
        # Esperar título Shopping Cart
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(ShoppingCartLocators.PAGE_TITLE)
        )
        # Screenshot final
        self.take_screenshot(test_name, "shopping_cart", suffix="after_page_load")

 # ... otros métodos existentes ...
    def open_product_pdp(self, category_name: str, test_name: str, random_product: bool = False):
        try:
            # Esperar productos en la PLP
            WebDriverWait(self.driver, 15).until(
                EC.visibility_of_all_elements_located(PlpLocators.PRODUCT_CARD)
            )
            products = self.driver.find_elements(*PlpLocators.PRODUCT_CARD)
            assert products, "No se encontraron productos en la PLP"
            # Selección de producto
            product = random.choice(products) if random_product else products[0]
            product_name = product.find_element(*PlpLocators.PRODUCT_NAME).text.strip()
            # Verificar si el producto está visible en viewport
            is_in_viewport = self.driver.execute_script("""
                var elem = arguments[0];
                var bounding = elem.getBoundingClientRect();
                return (
                    bounding.top >= 0 &&
                    bounding.left >= 0 &&
                    bounding.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
                    bounding.right <= (window.innerWidth || document.documentElement.clientWidth)
                );
            """, product)
            # Hacer scroll solo si no está visible
            if not is_in_viewport:
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                           product)
                time.sleep(0.5)
            # Screenshot del producto seleccionado en la PLP
            self.take_screenshot(test_name, category_name, suffix=f"before_click_{product_name}")
            # Click en "View Details"
            product.find_element(*PlpLocators.VIEW_DETAILS_BTN).click()
            # Esperar a que desaparezca el spinner
            try:
                WebDriverWait(self.driver, 15).until(
                    EC.invisibility_of_element_located(PlpLocators.SPINNER)
                )
            except TimeoutException:
                print("Spinner no desapareció a tiempo")
            # Esperar botón "Add to Cart" en PDP
            add_to_cart_btn = WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located(PlpLocators.pdp_add_to_cart_btn())
            )
            # Screenshot PDP cargada
            self.take_screenshot(test_name, category_name, suffix=f"pdp_{product_name}")
            # Validación
            assert add_to_cart_btn.is_displayed(), (
                f"No se encontró el botón 'Add to Cart' en la PDP del producto '{product_name}'"
            )
            print(f"PDP validada correctamente para producto: {product_name}")
            return product_name
        except Exception as e:
            # Screenshot en caso de error
            self.take_screenshot(test_name, category_name, suffix=f"error_{category_name}")
            raise e  # re-lanza el error para que pytest marque el test como fallido

    def assert_category_redirection(self, category_name: str):
        """Valida que al hacer clic en la categoría, la URL sea la correcta"""
        initial_url = self.driver.current_url
        self.go_to_category(category_name)

        WebDriverWait(self.driver, 10).until(
            lambda d: d.current_url != initial_url
        )
        current_url = self.driver.current_url

        # Usar el slug correcto desde el diccionario
        slug = CATEGORY_SLUGS[category_name]
        expected_url = f"{self.BASE_URL.rstrip('/')}/categories/{slug}"

        assert current_url != initial_url, f"No hubo redirección al hacer clic en {category_name}"
        assert current_url == expected_url, f"Redirección incorrecta: esperado {expected_url}, obtenido {current_url}"

        print(f"Redirección correcta a la categoría {category_name}: {current_url}")

    def assert_banner_visible(self):
        """Valida que el banner principal esté visible"""
        banner = self.driver.find_element(By.CSS_SELECTOR, ".plp-banner")
        assert banner.is_displayed(), "El banner no está visible en la PLP"

class ShoppingCartPage(BasePage):
    def assert_product_in_cart(self, product_name: str, test_name: str):
        try:
            # Esperar listado de productos
            WebDriverWait(self.driver, 15).until(
                EC.visibility_of_all_elements_located(ShoppingCartLocators.PRODUCT_NAMES)
            )
            product_names = [p.text.strip() for p in self.driver.find_elements(*ShoppingCartLocators.PRODUCT_NAMES)]

            if product_name not in product_names:
                self.take_screenshot(test_name, "shopping_cart", suffix=f"product_not_found_{product_name}")
                raise AssertionError(f"El producto '{product_name}' no se encuentra en el carrito")

            print(f"El producto '{product_name}' está en el carrito correctamente")

        except Exception as e:
            self.take_screenshot(test_name, "shopping_cart", suffix=f"error_assert_cart")
            raise e