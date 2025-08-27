# tests/users/conftest

import pytest

from API.utils.data import valid_email, valid_password, valid_full_name
from API.utils.user_helpers import _create_user, _build_user_data, delete_user_by_email, get_unique_email
from API.utils.settings import USERS


@pytest.fixture
def create_user_as_admin(auth_headers):
    unique_email = get_unique_email(prefix="create_user_as_admin_jasy")
    email = unique_email
    password = valid_password
    full_name = valid_full_name
    role = "admin"
    payload = _build_user_data(email, password, full_name, role)
    try:
        resp = _create_user(payload, auth_headers, path=USERS)
        return resp.status_code, resp.json()
    finally:
        delete_user = delete_user_by_email(email, auth_headers)

@pytest.fixture
def create_user_as_passenger(passenger_headers, auth_headers):
    unique_email = get_unique_email(prefix="create_user_as_passenger_jasy")
    email = unique_email
    password = valid_password
    full_name = valid_full_name
    role = "admin"
    payload = _build_user_data(email, password, full_name, role)
    try:
        resp = _create_user(payload, passenger_headers, path=USERS)
        return resp.status_code, resp.json()
    finally:
        delete_user = delete_user_by_email(email, auth_headers)



