import pytest
#Page Objects
from Web.pages.login_page import LoginPage
from Web.utils.data import VALID_USER_LOGIN, INVALID_USER_LOGIN
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By


#Precondición: carga el sitio web y redirige a la página de login
@pytest.fixture
def go_to_login_page(driver):
    login = LoginPage(driver)
    login.load()

@pytest.fixture
def clear_local_storage(driver):
    # Limpia local
    driver.execute_script("window.localStorage.clear();")

def test_redirects_to_login_page(driver):
    login = LoginPage(driver)
    login.load()

@pytest.mark.login_validCredentials
def test_login_with_valid_credentials(driver, go_to_login_page, clear_local_storage):
    #SETUP
    # Espera hasta que el overlay desaparezca
    login = LoginPage(driver)
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.fixed.inset-0.z-50"))
    )
    #EJECUCION
    # Ejemplo con un diccionario de datos
    # login.login_as_user(VALID_USER["email"], VALID_USER["password"])

    # EJECUCION usando un arreglo
    user = VALID_USER_LOGIN[0]
    login.login_as_user(user["email"],user["password"])
    # Espera hasta que el overlay desaparezca
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.fixed.inset-0.z-50"))
    )
    #VALIDACION
    login.assert_successful_login()

def test_login_with_capital_letters_email(driver, go_to_login_page, clear_local_storage):
    # SETUP
    # Espera hasta que el overlay desaparezca
    login = LoginPage(driver)
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.fixed.inset-0.z-50"))
    )
    # EJECUCION usando un arreglo
    user = VALID_USER_LOGIN[1]
    login.login_as_user(user["email"], user["password"])
    # Espera hasta que el overlay desaparezca
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.fixed.inset-0.z-50"))
    )
    # VALIDACION
    login.assert_successful_login()

#debe fallar hasta que se arregle el login inválido
def test_Login_with_invalid_password(driver, go_to_login_page, clear_local_storage):
    # SETUP
    # Espera hasta que el overlay desaparezca
    login = LoginPage(driver)
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.fixed.inset-0.z-50"))
    )
    # EJECUCION usando un arreglo
    user = INVALID_USER_LOGIN[0]
    login.login_as_user(user["email"], user["password"])
    # Espera hasta que el overlay desaparezca
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.fixed.inset-0.z-50"))
    )
    # VALIDACION
    login.assert_unsuccessful_login()

def test_login_with_empty_fields(driver, go_to_login_page, clear_local_storage):
    # SETUP
    # Espera hasta que el overlay desaparezca
    login = LoginPage(driver)
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.fixed.inset-0.z-50"))
    )
    # EJECUCION usando un arreglo
    user = INVALID_USER_LOGIN[1]
    login.login_as_user(user["email"], user["password"])
    # Espera hasta que el overlay desaparezca
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.fixed.inset-0.z-50"))
    )
    # VALIDACION
    login.assert_unsuccessful_login()

def test_login_invalid_email_format(driver, go_to_login_page, clear_local_storage):
    # SETUP
    # Espera hasta que el overlay desaparezca
    login = LoginPage(driver)
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.fixed.inset-0.z-50"))
    )
    # EJECUCION usando un arreglo
    user = INVALID_USER_LOGIN[2]
    login.login_as_user(user["email"], user["password"])
    # Espera hasta que el overlay desaparezca
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.fixed.inset-0.z-50"))
    )
    # VALIDACION
    login.assert_unsuccessful_login()

def test_login_with_unregistered_email(driver, go_to_login_page, clear_local_storage):
    # SETUP
    # Espera hasta que el overlay desaparezca
    login = LoginPage(driver)
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.fixed.inset-0.z-50"))
    )
    # EJECUCION usando un arreglo
    user = INVALID_USER_LOGIN[3]
    login.login_as_user(user["email"], user["password"])
    # Espera hasta que el overlay desaparezca
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.fixed.inset-0.z-50"))
    )
    # VALIDACION
    login.assert_unsuccessful_login()

def test_home_button_after_login(driver, go_to_login_page, clear_local_storage):
    # SETUP
    # Espera hasta que el overlay desaparezca
    login = LoginPage(driver)
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.fixed.inset-0.z-50"))
    )
    # EJECUCION
    # Ejemplo con un diccionario de datos
    # login.login_as_user(VALID_USER["email"], VALID_USER["password"])

    # EJECUCION usando un arreglo
    user = VALID_USER_LOGIN[0]
    login.login_as_user(user["email"], user["password"])
    # Espera hasta que el overlay desaparezca
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.fixed.inset-0.z-50"))
    )
    # VALIDACION
    login.assert_successful_login()

    # EJECUCION y validación
    login.assert_home_button_after_login()
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.fixed.inset-0.z-50"))
    )

def test_login_with_session_persistence(driver, go_to_login_page, clear_local_storage):
    # SETUP
    # Espera hasta que el overlay desaparezca
    login = LoginPage(driver)
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.fixed.inset-0.z-50"))
    )
    # EJECUCION
    # Ejemplo con un diccionario de datos
    # login.login_as_user(VALID_USER["email"], VALID_USER["password"])

    # EJECUCION usando un arreglo
    user = VALID_USER_LOGIN[0]
    login.login_as_user(user["email"], user["password"])
    # Espera hasta que el overlay desaparezca
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.fixed.inset-0.z-50"))
    )
    # VALIDACION
    login.assert_successful_login()

    # EJECUCION y validación
    login.assert_home_button_after_login()
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.fixed.inset-0.z-50"))
    )

    # Extrae la info de localStorage
    logged_user = driver.execute_script("return window.localStorage.getItem('loggedInUser');")

    # Validación: la sesión está activa si logged_user no es None
    assert logged_user is not None
    print("Usuario logueado:", logged_user)