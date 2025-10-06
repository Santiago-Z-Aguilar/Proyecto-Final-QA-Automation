#conftest va a definir los fixture que se va a compartir con pytest y pytest va a localizar esos
# fixtures para que se utilicen en todas las pruebas que generemos
from time import sleep
import pytest

from Web.utils.driver_factory import create_driver


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        help="ejecutar pruebas en modo headless (sin interfaz de usuario)"
    )

@pytest.fixture
def driver(request):
    headless = request.config.getoption("--headless")
    driver = create_driver(headless=headless)
    yield driver
    # sleep(2)
    driver.quit()

@pytest.fixture(scope="class")
def driver_class(request):
    headless = request.config.getoption("--headless")
    driver_class = create_driver(headless=headless)
    yield driver_class
    # sleep(2)
    driver_class.quit()