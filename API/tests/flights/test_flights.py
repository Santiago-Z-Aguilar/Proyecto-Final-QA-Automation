#from API.utils.user_helpers import create_user_with_email_already_registered
from API.utils.settings import USERS, USERS_ME
from API.utils.data import *
from API.utils.api_helpers import api_request

import requests
import pytest
from data import *
from conftest import _get_flight, auth_headers


# ---------- GET TESTS ----------
class TestFlightsGET:

    def test_get_success(self, base_url):
        resp = api_requests("get", FLIGHTS, headers=auth_headers())
        assert resp.status_code == 200, resp.text
        data = resp.json()
        assert isinstance(data, list)

    def test_get_flight_id(self, auth_headers): #obtner el id 
        status_code_create, detail_create = create_flight(data_post_success, auth_headers())
        assert status_code_create == 201
        assert "id" in resp.json()
        status_code_get, detail_get = get_flight_by_id(detail)
        assert resp.status_code == 200
        assert isinstance(resp.json(), dict)

