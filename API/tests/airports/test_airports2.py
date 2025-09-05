# from utils.api_helpers import api_request
# from utils.settings import AIRPORT, airport_schema
# from tests.airports.conftest import airport
# from jsonschema import validate
# from tests.conftest import auth_headers, admin_token
#
# def test_create_airport_schema(airport):
#     # airport ya es el JSON con la info creada
#     validate(instance=airport, schema=airport_schema)
#
# def test_get_all_airports(airport, auth_headers):
#     r = api_request("get", AIRPORT, headers=auth_headers)
#     assert r.status_code == 200
#     #
#     # airports = r.json()
#     assert isinstance(airports, list)
#     assert any(a["iata_code"] == airport["iata_code"] for a in airports)



