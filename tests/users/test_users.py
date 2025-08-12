from requests import RequestException
from tests.users.conftest import user_fixture
from utils.settings import user_schema, USERS
import pytest
from jsonschema import validate
import time
from tests.conftest import auth_headers, api_request, admin_token

# @pytest.mark.parametrize('user_fixture', ['admin'], indirect=True)
# def test_create_admin_user(auth_headers, user_fixture):
#     assert user_fixture["role"] == "admin"
#     print(user_fixture)
#
#
# @pytest.mark.parametrize('user_fixture', ['passenger'], indirect=True)
# def test_create_passenger_user(auth_headers, user_fixture):
#     assert user_fixture["role"] == "passenger"
#     print(user_fixture)
#
# @pytest.mark.parametrize("user_fixture", ["admin"], indirect=True)
# def test_validate_user_schema(user_fixture):
#     admin_user = user_fixture
#     assert admin_user["role"] == "admin"
#
#
# def test_get_all_users(auth_headers):
#     r = api_request("get", USERS, headers=auth_headers)
#     print("⚠️ STATUS:", r.status_code)
#     print("📨 BODY:", r.text)
#     assert r.status_code == 200

