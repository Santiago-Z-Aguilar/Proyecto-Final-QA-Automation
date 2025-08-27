# tests/users/test_users

from API.utils.user_helpers import create_user_with_email_already_registered
from API.utils.settings import USERS
from API.utils.data import passenger_role, admin_role, invalid_role, emails_to_test


# ---------- Existing user ----------
def test_user_with_email_already_registered(auth_headers):
    status_code, detail = create_user_with_email_already_registered(auth_headers, USERS, role='admin')
    assert status_code == 400


def test_create_admin_user_as_admin(auth_headers, create_user_as_admin):
    role = admin_role
    status_code, detail = create_user_as_admin(role=role)
    assert status_code == 201
    assert role in detail['role'], f'Expected role {role}, but got {detail['role']}'

def test_create_passenger_user_as_admin(auth_headers, create_user_as_admin):
    role = passenger_role
    status_code, detail = create_user_as_admin(role=role)
    assert status_code == 201
    assert role in detail['role'], f'Expected role {role}, but got {detail['role']}'


def test_create_admin_user_as_passenger(auth_headers, passenger_headers, create_user_as_passenger):
    role = admin_role
    status_code, detail = create_user_as_passenger(role=role)
    assert status_code == 403
    assert "Admin privileges required" in detail["detail"]

def test_create_passenger_user_as_passenger(auth_headers, passenger_headers, create_user_as_passenger):
    role = passenger_role
    status_code, detail = create_user_as_passenger(role=role)
    assert status_code == 403
    assert "Admin privileges required" in detail["detail"]

def test_create_user_with_invalid_role_value(auth_headers, create_user_as_admin):
    role = invalid_role
    status_code, detail = create_user_as_admin(role=role)
    assert status_code == 422
    expected_roles_response = detail["detail"][0]["ctx"]["expected"]
    assert passenger_role and admin_role in expected_roles_response

# def test_create_user_with_invalid_email_format(auth_headers, create_user_as_admin):
#     expected_status = next(c["expected_status"] for c in emails_to_test if c["email"] == invalid_email)
#
#     status_code, detail = create_user_as_admin(email=invalid_email)
#     assert  status_code = 422
