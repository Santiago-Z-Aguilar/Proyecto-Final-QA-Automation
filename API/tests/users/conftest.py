# tests/users/conftest

import pytest

from API.utils.data import valid_password, valid_full_name, admin_role, passenger_role
from API.utils.user_helpers import _create_user, _build_user_data, delete_user_by_email, get_unique_email
from API.utils.settings import USERS


@pytest.fixture
def create_user_as_admin(auth_headers):
    """Crea un usuario como admin y lo elimina al terminar."""
    created_email = None

    def _create(email: str = None, role: str = admin_role):
        nonlocal created_email
        if email is None:
            email = get_unique_email(prefix="admin_user_jasy")
        payload = _build_user_data(email, valid_password, valid_full_name, role)
        resp = _create_user(payload, auth_headers, path=USERS)
        created_email = email
        return resp.status_code, resp.json()

    yield _create

    if created_email:
        delete_user_by_email(created_email, auth_headers)


@pytest.fixture
def create_user_as_passenger(auth_headers, passenger_headers):
    """Crea un usuario como pasajero y lo elimina al terminar."""
    created_email = None

    def _create(email: str = None, role: str = passenger_role):
        nonlocal created_email
        if email is None:
            email = get_unique_email(prefix="passenger_user_jasy")
        payload = _build_user_data(email, valid_password, valid_full_name, role)
        resp = _create_user(payload, passenger_headers, path=USERS)
        created_email = email
        return resp.status_code, resp.json()

    yield _create

    if created_email:
        delete_user_by_email(created_email, auth_headers)




