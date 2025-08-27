from API.utils.user_helpers import create_user_with_email_already_registered
from API.utils.settings import USERS

def test_create_user_as_admin(auth_headers, create_user_as_admin):
    status_code, detail = create_user_as_admin

    assert status_code == 201
    assert "admin" in detail['role']

# ---------- Existing user ----------
def test_signup_with_existing_user(auth_headers):
    status_code, detail = create_user_with_email_already_registered(auth_headers, USERS, role='admin')
    assert status_code == 400
