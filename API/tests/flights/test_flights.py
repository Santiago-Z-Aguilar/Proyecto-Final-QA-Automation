from API.tests.flights.data_fligths import *
from API.utils.flights_helpers import *


# crear aircrafts

# ---------- POST TESTS ----------
class TestFlightsPOST:

    def test_create_flight_success(self, auth_headers, base_flight_data):
        resp = create_flight(base_flight_data, auth_headers)
        assert resp.status_code == 201, f"Expected 201, got {status_code}. Response: {detail}"

    def test_create_flight_invalid_origin(self, auth_headers, with_aircraft_id):
        payload = with_aircraft_id(data_post_invalid_origin)
        resp = create_flight(payload, auth_headers)
        assert resp.status_code == 422, f"Expected 422, got {status_code}. Response: {detail}"

    def test_create_flight_empty_origin(self, auth_headers, with_aircraft_id):
        payload = with_aircraft_id(data_post_origin_empty)
        resp = create_flight(payload, auth_headers)
        assert resp.status_code == 422, f"Expected 422, got {status_code}. Response: {detail}"

    def test_create_flight_none_origin(self, auth_headers, with_aircraft_id):
        payload = with_aircraft_id(data_post_origin_none)
        resp = create_flight(payload, auth_headers)
        assert resp.status_code == 422, f"Expected 422, got {status_code}. Response: {detail}"

    def test_create_flight_invalid_destination(self, auth_headers, with_aircraft_id):
        payload = with_aircraft_id(data_post_destination_invalid)
        resp = create_flight(payload, auth_headers)
        assert resp.status_code == 422, f"Expected 422, got {status_code}. Response: {detail}"

    def test_create_flight_origin_destination_same(self, auth_headers, with_aircraft_id):
        payload = with_aircraft_id(data_post_origin_dest_same)
        resp = create_flight(payload, auth_headers)
        assert resp.status_code == 422, f"Expected 422, got {resp.status_code}. Comment: Origin and destination cannot be the same"

    def test_create_flight_departure_in_past(self, auth_headers, with_aircraft_id):
        payload = with_aircraft_id(data_post_departure_in_past)
        resp = create_flight(payload, auth_headers)
        assert resp.status_code == 422, f"Expected 422, got {resp.status_code}. Comment: arrival_time must occur after departure_date"

    def test_create_flight_negative_price(self, auth_headers, with_aircraft_id):
        payload = with_aircraft_id(data_post_negative_price)
        resp = create_flight(payload, auth_headers)
        assert resp.status_code == 422, f"Expected 422, got {resp.status_code}."

    def test_create_flight_zero_price(self, auth_headers, with_aircraft_id):
        payload = with_aircraft_id(data_post_zero_price)
        resp = create_flight(payload, auth_headers)
        assert resp.status_code == 422, f"Expected 422, got {resp.status_code}. Comment: Price cannot be zero"
        
    def test_create_flight_nonnumeric_price(self, auth_headers, with_aircraft_id):
        payload = with_aircraft_id(data_post_nonumeric_price)
        resp = create_flight(payload, auth_headers)
        assert resp.status_code == 422, f"Expected 422, got {status_code}. Comment: Price should be a float"
        
    def test_create_flight_int_price(self, auth_headers, with_aircraft_id):
        payload = with_aircraft_id(data_post_int_price)
        resp = create_flight(payload, auth_headers)
        assert resp.status_code == 201, f"Expected 201, got {status_code}. Comment: Accept. Price should be a float "
        
    def test_create_flight_30digits_price(self, auth_headers, with_aircraft_id):
        payload = with_aircraft_id(data_post_30digits_price)
        resp = create_flight(payload, auth_headers)
        assert resp.status_code == 201, f"Expected 201, got {status_code}. Comment: Accept. Price should be a float "


    def test_create_nonexistent_aircraft(self, auth_headers, nonexistent_aircraft_id):
        payload = data_post_nonexistent_aircraft.copy()
        payload["aircraft_id"] = nonexistent_aircraft_id
        resp = create_flight(payload, auth_headers)
        assert resp.status_code == 404, f"Expected 404, got {resp.status_code}. Response: {resp.text} Aircraft not found"

    def test_create_empty_aircraft(self, auth_headers, empty_aircraft_id):
        payload = data_post_empty_aircraft.copy()
        payload["aircraft_id"] = empty_aircraft_id
        resp = create_flight(payload, auth_headers)
        detail = assert_response(resp, 422)
        assert "aircraft" in str(detail).lower()

    def test_create_number_aircraft(self, auth_headers, numeric_aircraft_id):
        payload = data_post_number_aircraft.copy()
        payload["aircraft_id"] = numeric_aircraft_id
        resp = create_flight(payload, auth_headers)
        detail = assert_response(resp, 422)
        assert "aircraft" in str(detail).lower()

    def test_create_fields_missing(self, auth_headers, with_aircraft_id):
        payload = with_aircraft_id(data_post_fields_missing)
        resp = create_flight(payload, auth_headers)
        assert resp.status_code == 422, f"Expected 201, got {status_code}. "
    
    def test_create_json_disarray(self, auth_headers, with_aircraft_id):
        payload = with_aircraft_id(data_post_json_disarray)
        resp = create_flight(payload, auth_headers)
        assert resp.status_code == 201, f"Expected 201, got {status_code}. "
        resp_get = get_flight_by_id(resp.json()["id"])
        assert resp_get.status_code == 200, f"Expected 200, got {resp_get.status_code}. Response: {resp_get.text}"
        fetched = resp_get.json()
        assert fetched["origin"] == payload["origin"], (
            f"Expected origin {payload['origin']}, got {fetched['origin']}"
        )



# ---------- GET TESTS ----------
class TestFlightsGET:

    def test_get_success(self):
       resp = get_flights()
       assert resp.status_code == 200, f"Expected 200, got {status_code}. Response: {detail} Server Error"

    def test_get_flight_id(self, flight_id):
        resp_get = get_flight_by_id(flight_id)
        assert resp_get.status_code == 200, f"Expected 200, got {resp_get.status_code}. Response: {detail}"
        assert isinstance(resp_get.json(), dict)

    def test_get_nonexistent_flight(self, auth_headers, fake_flight_id):
        resp = get_flight_by_id(fake_flight_id)
        assert resp.status_code == 404, f"Expected 404, got {resp.status_code}"


    def test_get_invalid_flight_id(self, auth_headers, invalid_flight_id):
        resp = get_flight_by_id(invalid_flight_id)
        assert resp.status_code == 404, f"Expected 404, got {resp.status_code}"

# ---------- PUT TESTS ----------
class TestFlightsPUT:

    def test_update_flight_success(self, auth_headers, create_flight, with_aircraft_id):
        flight_id = create_flight["id"] #Create flight
        payload = with_aircraft_id(data_put_valid)
        resp_put = update_flight(flight_id, payload, auth_headers)
        assert resp_put.status_code == 200, f"Expected 200, got {resp_put.status_code}. Response: {resp_put.text}"

    def test_update_invalid_origin(self, auth_headers, flight_id, with_aircraft_id):
        payload = with_aircraft_id(data_put_invalid_origin)
        resp_put = update_flight(flight_id, payload, auth_headers)
        assert resp_put.status_code == 422, f"Expected 422, got {resp_put.status_code}. Response: {resp_put.text}"

    def test_update_invalid_destination(self, auth_headers, flight_id, with_aircraft_id):
        payload = with_aircraft_id(data_put_invalid_destinationn)
        resp_put = update_flight(flight_id, payload, auth_headers)
        assert resp_put.status_code == 422, f"Expected 422, got {resp_put.status_code}. Response: {resp_put.text}"

    def test_update_departure_past(self, auth_headers, flight_id, with_aircraft_id):
        payload = with_aircraft_id(data_put_arrival_before_dep)
        resp_put = update_flight(flight_id, payload, auth_headers)
        assert resp_put.status_code == 422, (f"Expected 422, got {resp_put.status_code}. "
                                             f"Response: {resp_put.text} arrival_time must occur after departure_date")

    def test_update_zero_price(self, auth_headers, flight_id, with_aircraft_id):
        payload = with_aircraft_id(data_put_zero_price )
        resp_put = update_flight(flight_id, payload, auth_headers)
        assert resp_put.status_code == 422, (f"Expected 422, got {resp_put.status_code}. "
                                             f"Response: {resp_put.text} Price cannot be zero")

    def test_update_negative_price(self, auth_headers, flight_id, with_aircraft_id):
        payload = with_aircraft_id(data_put_negative_price)
        resp_put = update_flight(flight_id, payload, auth_headers)
        assert resp_put.status_code == 422, (f"Expected 422, got {resp_put.status_code}. "
                                             f"Response: {resp_put.text} Price cannot be zero")

    def test_update_negative_price(self, auth_headers, flight_id, with_aircraft_id):
        payload = with_aircraft_id(data_put_negative_price)
        resp_put = update_flight(flight_id, payload, auth_headers)
        assert resp_put.status_code == 422, (f"Expected 422, got {resp_put.status_code}. "
                                             f"Response: {resp_put.text} Price should be a positive float")

    def test_update_float_price(self, auth_headers, flight_id, with_aircraft_id):
        payload = with_aircraft_id(data_put_float_price)
        resp_put = update_flight(flight_id, payload, auth_headers)
        assert resp_put.status_code == 200, f"Expected 200, got {resp_put.status_code}.Response: {resp_put.text}"
        resp_get = get_flight_by_id(flight_id) #Get flight
        assert resp_get.status_code == 200, f"Expected 200, got {resp_get.status_code}. Response: {resp_get.text}"
        flight = resp_get.json()
        assert flight["base_price"] == payload["base_price"], (
            f"Expected base_price {payload['base_price']}, got {flight['base_price']}"
        )

    def test_update_30digit_price(self, auth_headers, flight_id, with_aircraft_id):
        payload = with_aircraft_id(data_put_price_30digits)
        resp_put = update_flight(flight_id, payload, auth_headers)
        assert resp_put.status_code == 200, f"Expected 200, got {resp_put.status_code}.Response: {resp_put.text}"
        resp_get = get_flight_by_id(flight_id) #Get flight
        assert resp_get.status_code == 200, (f"Expected 200, got {resp_get.status_code}. Response: {resp_get.text}")
        flight = resp_get.json()
        assert flight["base_price"] == payload["base_price"], (
            f"Expected base_price {payload['base_price']}, got {flight['base_price']}"
        )

    def test_update_nonexistent_aircraft(self, auth_headers, flight_id, nonexistent_aircraft_id):
        payload = data_post_nonexistent_aircraft.copy()
        payload["aircraft_id"] = nonexistent_aircraft_id
        resp_put = update_flight(flight_id, payload, auth_headers)
        assert resp_put.status_code == 404, f"Expected 404, got {resp.status_code}. Response: {resp.text} Aircraft not found"

# ---------- DELETE TESTS ----------
class TestFlightsDELETE:

    def test_create_flight_success(self, auth_headers, base_flight_data):
        resp = create_flight(base_flight_data, auth_headers)
        assert resp.status_code == 201

    def test_delete_flight_success(self, auth_headers, flight_id):
        assert flight_id is not None
        resp_delete = delete_flight(flight_id, auth_headers)
        assert resp_delete.status_code == 204, (f"Expected 204, got {resp_delete.status_code}. "
                                                f"Response: {resp_delete.text}")
        resp_get = get_flight_by_id(flight_id)
        assert resp_get.status_code == 404, (
            f"Expected 404 after deletion, got {resp_get.status_code}. Response: {resp_get.text}"
        )

    def test_delete_nonexistent_flight(self,auth_headers, fake_flight_id):
        resp_delete = delete_flight(fake_flight_id, auth_headers)
        assert resp_delete.status_code == 404, (
            f"Expected 404, got {resp_delete.status_code}. Response: {resp_delete.text}"
        )

    def test_delete_invalid_flight(self, auth_headers, invalid_flight_id):
        resp_delete = delete_flight(invalid_flight_id, auth_headers)
        assert resp_delete.status_code == 404, (
            f"Expected 404, got {resp_delete.status_code}. Response: {resp_delete.text}"
        )
        