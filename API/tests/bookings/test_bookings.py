import pytest
from API.utils.bookings_helpers import create_valid_booking
from API.utils.data import passengers_to_test,flights_to_test,pagination_values_to_test,two_passengers_payload
from jsonschema import validate
from API.utils.settings import booking_schema

class TestBookings:
    # POST
    @pytest.mark.parametrize("passenger_case", passengers_to_test)
    def test_create_booking_passenger_validation(self,create_booking_passenger_case,passenger_case):
        response = create_booking_passenger_case(passenger_case["passengers"])
        assert response.status_code == passenger_case["expected_status"]

    @pytest.mark.parametrize("flight_case", flights_to_test)
    def test_create_booking_flight_validation(self,create_booking_flight_case,flight_case):
        response = create_booking_flight_case(flight_case["flight_id"])
        assert response.status_code == flight_case["expected_status"]

    # GET
    @pytest.mark.parametrize("pagination_case", pagination_values_to_test)
    def test_list_bookings(self,list_bookings,pagination_case):
        response = list_bookings(pagination_case["skip"],pagination_case["limit"])
        assert response.status_code == pagination_case["expected_status"]

    def test_get_own_booking_passenger(self,get_booking,create_valid_booking_as_passenger,passenger_headers):
        booking_id = create_valid_booking_as_passenger["id"]
        response = get_booking(booking_id,passenger_headers)
        assert response.status_code == 200

    def test_get_other_user_booking(self,get_booking,auth_headers,passenger_headers):
        booking_id = create_valid_booking(auth_headers)["id"]
        response = get_booking(booking_id,passenger_headers)
        assert response.status_code == 403

    def test_get_booking_without_token(self,get_booking,auth_headers):
        booking_id = create_valid_booking(auth_headers)["id"]
        response = get_booking(booking_id,None)
        assert response.status_code == 401

    def test_get_booking_admin(self,get_booking,auth_headers,create_valid_booking_as_passenger):
        booking_id = create_valid_booking_as_passenger["id"]
        response = get_booking(booking_id,auth_headers)
        assert response.status_code == 200

    def test_get_invalid_token(self,get_booking,auth_headers):
        booking_id = "lpb-235asd68"
        response = get_booking(booking_id,auth_headers)
        assert response.status_code == 404

    # PATCH
    @pytest.mark.parametrize("update_case",[
        {"case":{"passengers": two_passengers_payload},"expected_status":200},
        {"case":{'flight_id' : '123'},"expected_status":200},
        {"case":{'user_id' : '123'},"expected_status":200},
        {"case":{'id' : '123'},"expected_status":403},
        {"case":{'status' : 'paid'},"expected_status":200},
        {"case":{'status' : '123'},"expected_status":400},
    ])
    def test_update_booking(self,update_case,auth_headers,update_booking):
        booking_id = create_valid_booking(auth_headers)["id"]
        response = update_booking(booking_id,update_case["case"],auth_headers)
        assert response.status_code == update_case["expected_status"]

    # DELETE
    def test_delete_own_booking_passenger(self,passenger_headers,delete_booking,create_valid_booking_as_passenger):
        booking_id = create_valid_booking_as_passenger["id"]
        response = delete_booking(booking_id,passenger_headers)
        assert response.status_code == 204

    def test_delete_other_user_booking(self,delete_booking,auth_headers,passenger_headers):
        booking_id = create_valid_booking(auth_headers)["id"]
        response = delete_booking(booking_id,passenger_headers)
        assert response.status_code == 403

    def test_delete_booking_without_token(self,delete_booking,auth_headers):
        booking_id = create_valid_booking(auth_headers)["id"]
        response = delete_booking(booking_id,None)
        assert response.status_code == 401

    def test_delete_invalid_token(self,delete_booking,auth_headers):
        booking_id = "lpb-235asd68"
        response = delete_booking(booking_id,auth_headers)
        assert response.status_code == 404


    #Schema test

    def test_aircraft_schema(self,auth_headers,get_booking):
        booking_id = create_valid_booking(auth_headers)["id"]
        response = get_booking(booking_id,auth_headers)
        validate(instance=response.json(), schema=booking_schema)


