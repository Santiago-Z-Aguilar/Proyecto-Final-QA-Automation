import random
import pytest
from Web.locators.plp_locators import PlpLocators
from Web.pages.plp_page import PlpPage
from Web.utils.data import CATEGORIES, CATEGORY_DESCRIPTIONS
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from Web.pages.plp_page import ShoppingCartPage


# ========================
# POSITIVE TEST CASES
# ========================

"""Verify that the category title is displayed correctly in the PLP"""
@pytest.mark.parametrize("category_name", CATEGORIES.values())
def test_category_title(driver, category_name):
    plp_page = PlpPage(driver)
    plp_page.load_home()
    plp_page.go_to_category(category_name)
    plp_page.assert_category_title(category_name)
    plp_page.take_screenshot("test_category_title", category_name)

"""Verify that the category description is displayed correctly in the PLP"""
@pytest.mark.parametrize("category_name", CATEGORIES.values())
def test_category_description(driver, category_name):
    plp_page = PlpPage(driver)
    plp_page.load_home()
    plp_page.go_to_category(category_name)
    expected_description = CATEGORY_DESCRIPTIONS[category_name]
    plp_page.assert_category_description(expected_description)
    plp_page.take_screenshot("test_category_description", category_name)

"""Verify that all products in the category are displayed correctly in the PLP"""
@pytest.mark.parametrize("category_name", CATEGORIES.values())
def test_all_products_display(driver, category_name):
    plp_page = PlpPage(driver)
    plp_page.load_home()
    plp_page.go_to_category(category_name)
    plp_page.assert_products_display(category_name, "test_all_products_display")

"""Verify that when clicking on the view details button of a product in the PLP, the product's PDP is loaded correctly"""
@pytest.mark.parametrize("category_name", CATEGORIES.values())
def test_view_details_opens_pdp(driver, category_name):
    plp_page = PlpPage(driver)
    plp_page.load_home()
    plp_page.go_to_category(category_name)
    plp_page.open_product_pdp(category_name, test_name="test_view_details_opens_pdp", random_product=True)

"""Verify that clicking on a product's add to cart button, updates the quantity in the header cart and adds the product to the cart"""
@pytest.mark.parametrize("category_name", CATEGORIES.values())
def test_add_to_cart_from_plp(driver, category_name):
    plp_page = PlpPage(driver)
    cart_page = ShoppingCartPage(driver)
    plp_page.load_home()
    plp_page.go_to_category(category_name)
    product_name = plp_page.add_random_product_to_cart(
        test_name="test_add_to_cart",
        category_name=category_name
    )
    plp_page.open_cart_and_wait(test_name="test_add_to_cart")
    cart_page.assert_product_in_cart(product_name, test_name="test_add_to_cart")

# ========================
# NEGATIVE TEST CASES
# ========================

@pytest.mark.negative
def test_invalid_category(driver):
    """
    Caso negativo: validar que al intentar acceder a una categoría inexistente
    la app no se rompa y no muestre productos.
    """
    from Web.pages.plp_page import PlpPage
    from Web.locators.plp_locators import PlpLocators
    plp_page = PlpPage(driver)
    plp_page.load_home()
    invalid_category = "Kids Clothes"
    slug = invalid_category.lower().replace(" ", "-")
    invalid_url = f"{plp_page.BASE_URL.rstrip('/')}/categories/{slug}"
    driver.get(invalid_url)
    # Esperar unos segundos por si hay render
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located(PlpLocators.PRODUCT_CARD)
        )
        products = driver.find_elements(*PlpLocators.PRODUCT_CARD)
    except:
        products = []
    assert len(products) == 0, f"La categoría inválida debería mostrar 0 productos: {invalid_url}"

@pytest.mark.negative
def test_category_images_do_not_load(driver):
    """
    Caso negativo: forzar que las imágenes de 'Comprar por categorías' no se carguen
    y validar que realmente no se cargan.
    """
    driver.get("https://shophub-commerce.vercel.app")
    wait = WebDriverWait(driver, 10)
    for key, category_name in CATEGORIES.items():
        # Localizar la imagen por su alt
        img_element = wait.until(
            EC.presence_of_element_located((By.XPATH, f"//img[@alt={repr(category_name)}]"))
        )
        # Forzar que la imagen no se cargue (src inválido)
        driver.execute_script("arguments[0].src='invalid.jpg';", img_element)
        # Validar que la imagen no se cargó
        is_loaded = driver.execute_script(
            "return arguments[0].complete && arguments[0].naturalWidth > 0;", img_element
        )
        assert not is_loaded, f"La imagen de '{category_name}' se cargó inesperadamente."


@pytest.mark.negative
@pytest.mark.parametrize("category_name", CATEGORIES.values())
def test_missing_category_title(driver, category_name):
    """
    Caso negativo: Inducir la ausencia del H1 (título de categoría)
    y validar que el test detecta el fallo.
    """
    plp_page = PlpPage(driver)
    plp_page.load_home()
    plp_page.go_to_category(category_name)
    # Inducir falla: eliminar H1 del DOM
    try:
        title_element = driver.find_element(*PlpLocators.category_title_locator(category_name))
        driver.execute_script("arguments[0].remove();", title_element)
    except Exception:
        # Si no existe, ya cumple el escenario negativo
        pass
    # El assert debería fallar al intentar validar el título
    import pytest
    with pytest.raises(Exception):
        plp_page.assert_category_title(category_name)


@pytest.mark.negative
@pytest.mark.parametrize("category_name", CATEGORIES.values())
def test_category_click_no_redirect_from_home(driver, category_name):
    """
    Caso negativo: desde Home > Shop by Category, hacer clic en la categoría
    y validar que NO redirige a la PLP (clic no funcional forzado).
    """
    driver.get("https://shophub-commerce.vercel.app")  # Abrir Home
    initial_url = driver.current_url
    wait = WebDriverWait(driver, 10)  # Espera hasta 10 segundos
    # XPath del h3 que contiene el nombre de la categoría
    xpath_locator = f"//div[h3[text()={repr(category_name)}]]/h3"
    # Esperar a que el elemento sea visible
    category_element = wait.until(
        EC.visibility_of_element_located((By.XPATH, xpath_locator))
    )
    # Inducir fallo: deshabilitar el clic del enlace (previene navegación)
    driver.execute_script("""
        const el = arguments[0];
        const parentLink = el.closest('a');
        if(parentLink) {
            parentLink.removeAttribute('href');
            parentLink.onclick = function(e){ e.preventDefault(); };
        }
    """, category_element)
    # Hacer clic en la categoría
    category_element.click()
    # Esperar a que el navegador procese el clic (la URL no debería cambiar)
    wait.until(lambda driver: driver.current_url is not None)
    # Validar que la URL no cambió
    current_url = driver.current_url
    assert current_url == initial_url, f"La categoría '{category_name}' redirigió inesperadamente a {current_url}"

@pytest.mark.negative
@pytest.mark.parametrize("category_name", CATEGORIES.values())
def test_category_redirects_to_random_wrong_plp(driver, category_name):
    """
    Caso negativo: al hacer clic en cada categoría desde Home,
    forzar que redirija a otra PLP aleatoria diferente y validar que la URL es incorrecta.
    """
    driver.get("https://shophub-commerce.vercel.app")  # Abrir Home
    wait = WebDriverWait(driver, 10)
    # XPath del h3 que contiene el nombre de la categoría
    xpath_locator = f"//div[h3[text()={repr(category_name)}]]/h3"
    # Esperar a que el elemento sea visible y clickeable
    category_element = wait.until(
        EC.element_to_be_clickable((By.XPATH, xpath_locator))
    )
    # Elegir una categoría diferente al azar usando los valores del diccionario
    other_categories = [c for c in CATEGORIES.values() if c != category_name]
    wrong_category = random.choice(other_categories)
    wrong_url = f"https://shophub-commerce.vercel.app/categories/{wrong_category.lower().replace(' ', '-')}"
    # Forzar la redirección usando JS
    driver.execute_script(
        """
        const elem = arguments[0];
        const wrongUrl = arguments[1];
        elem.addEventListener('click', function(e){
            e.preventDefault();
            window.location.href = wrongUrl;
        });
        """,
        category_element,
        wrong_url
    )
    # Guardar URL inicial
    initial_url = driver.current_url
    # Hacer clic en la categoría
    category_element.click()
    # Esperar a que la URL cambie
    wait.until(lambda d: d.current_url != initial_url)
    # Validar que redirigió a la URL incorrecta
    current_url = driver.current_url
    assert current_url == wrong_url, (
        f"La categoría '{category_name}' no redirigió a la URL incorrecta esperada. "
        f"URL actual: {current_url}"
    )