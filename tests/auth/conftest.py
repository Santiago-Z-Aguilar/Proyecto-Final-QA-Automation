import logging
from typing import Any, Dict, Optional, Tuple
from uuid import uuid4
import pytest

from tests.auth.data import valid_password, valid_full_name
from utils.api_helpers import api_request
from utils.settings import AUTH_LOGIN
from utils.user_helpers import (
    get_user_by_email,
    delete_user_by_email,
    user_exist_skip,
    _create_user,
)

# ---------- Logging ----------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("qa_tests")


# ---------- Helpers ----------
def _unique_email(prefix: str = "t") -> str:
    """Genera un email único con UUID, seguro para ejecución en paralelo."""
    return f"{prefix}_{uuid4().hex}@example.com"

def _build_data(email: str, password: str, full_name: str, role: Optional[str] = None) -> Dict[str, Any]:
    """Construye la data de creación de usuario."""
    data = {"email": email, "password": password, "full_name": full_name}
    if role is not None:
        data["role"] = role
    return data

def _assert_status(resp, expected_status: int, context: Dict[str, Any]) -> None:
    """Valida que el status code sea el esperado."""
    assert resp is not None, "API response is None"
    assert resp.status_code == expected_status, (
        f"\n---\nTest failed for {context}\n"
        f"Expected: {expected_status} | Actual: {resp.status_code}\n"
        f"Response: {getattr(resp, 'text', '<no text>')}\n---"
    )

def _signup_case(case: Dict[str, Any], auth_headers, prefix: str) -> Tuple[Any, str, Optional[Dict[str, Any]]]:
    """Lógica común para crear usuario y hacer cleanup híbrido."""
    email = case.get("email", _unique_email(prefix=prefix))
    password = case.get("password", valid_password)
    full_name = case.get("full_name", valid_full_name)
    expected_status = case["expected_status"]

    # Solo verificar existencia previa si esperamos éxito
    if expected_status == 201:
        user_exist_skip(email, auth_headers)

    data = _build_data(email, password, full_name)

    resp = None
    try:
        resp = _create_user(data, auth_headers)
        _assert_status(resp, expected_status, case)

        # Obtener usuario solo si fue 201
        user = get_user_by_email(email, auth_headers) if resp.status_code == 201 else None
        return resp, email, user
    finally:
        # Cleanup híbrido:
        # 1. Si API devolvió 201 → borrar
        # 2. Si API devolvió otro código pero usuario existe → borrar igual
        try:
            existing_user = None
            if resp and resp.status_code == 201:
                existing_user = True
            else:
                # Buscar usuario solo si podría haberse creado
                existing_user = get_user_by_email(email, auth_headers) is not None

            if existing_user:
                deleted = delete_user_by_email(email, auth_headers)
                logger.info(f"Cleanup: {'✅' if deleted else '❌'} User '{email}' deleted")
        except Exception as e:
            logger.warning(f"Cleanup exception for '{email}': {e}")


# ---------- Fixtures por campo ----------
@pytest.fixture
def signup_email_case(auth_headers):
    """Fixture para probar validaciones de email."""
    def _signup_email(case: Dict[str, Any]):
        return _signup_case(case, auth_headers, prefix="emailtest")
    return _signup_email

@pytest.fixture
def signup_password_case(auth_headers):
    """Fixture para probar validaciones de password."""
    def _signup_password(case: Dict[str, Any]):
        return _signup_case(case, auth_headers, prefix="pwtest")
    return _signup_password

@pytest.fixture
def signup_full_name_case(auth_headers):
    """Fixture para probar validaciones de full_name."""
    def _signup_fullname(case: Dict[str, Any]):
        return _signup_case(case, auth_headers, prefix="nametest")
    return _signup_fullname


# ---------- Otros fixtures ----------
@pytest.fixture
def signup_with_custom_role(auth_headers):
    """Fixture para crear usuarios con rol personalizado (sin validación)."""
    def _signup(role: str, prefix: str = "role_test"):
        test_email = _unique_email(prefix)
        data = _build_data(test_email, valid_password, valid_full_name, role=role)

        resp = None
        try:
            resp = _create_user(data, auth_headers)
            _assert_status(resp, 201, {"attempted_role": role})
            return get_user_by_email(test_email, auth_headers)
        finally:
            try:
                existing_user = get_user_by_email(test_email, auth_headers) is not None
                if existing_user:
                    deleted = delete_user_by_email(test_email, auth_headers)
                    logger.info(f"Cleanup: {'✅' if deleted else '❌'} User '{test_email}' deleted")
            except Exception as e:
                logger.warning(f"Cleanup exception for '{test_email}': {e}")
    return _signup

@pytest.fixture
def signup_with_valid_data(auth_headers):
    """Fixture para crear un usuario válido con cleanup automático."""
    unique_email = _unique_email(prefix="valid_user")
    data = _build_data(unique_email, valid_password, valid_full_name)

    user_exist_skip(unique_email, auth_headers)
    resp = None
    try:
        resp = _create_user(data, auth_headers)
        _assert_status(resp, 201, data)
        user = get_user_by_email(unique_email, auth_headers)
        yield user
    finally:
        try:
            existing_user = get_user_by_email(unique_email, auth_headers) is not None
            if existing_user:
                deleted = delete_user_by_email(unique_email, auth_headers)
                logger.info(f"Cleanup: {'✅' if deleted else '❌'} User '{unique_email}' deleted")
        except Exception as e:
            logger.warning(f"Cleanup exception for '{unique_email}': {e}")


# ---------- Authentication helpers ----------
def login(user: str, password: str):
    """Realiza login y retorna la respuesta."""
    response = api_request("post", AUTH_LOGIN, data={"username": user, "password": password})
    if response is None:
        raise Exception("Login failed after retries")
    if response.status_code not in (200, 401):
        raise Exception(f"Unexpected status: {response.status_code}, Response: {response.text}")
    return response

def login_as_passenger(auth_headers):
    """Crea un pasajero y realiza login."""
    unique_email = _unique_email(prefix="passenger_test")
    data = _build_data(unique_email, valid_password, valid_full_name)

    resp = None
    try:
        resp = _create_user(data, auth_headers)
        _assert_status(resp, 201, data)

        user = get_user_by_email(unique_email, auth_headers)
        assert user["role"] == "passenger"

        return login(unique_email, valid_password)
    finally:
        try:
            existing_user = get_user_by_email(unique_email, auth_headers) is not None
            if existing_user:
                deleted = delete_user_by_email(unique_email, auth_headers)
                logger.info(f"Cleanup: {'✅' if deleted else '❌'} User '{unique_email}' deleted")
        except Exception as e:
            logger.warning(f"Cleanup exception for '{unique_email}': {e}")
