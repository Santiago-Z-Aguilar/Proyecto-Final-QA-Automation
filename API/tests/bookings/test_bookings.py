import pytest

from API.tests.bookings.conftest import create_booking_flight_case
from API.utils.data import passengers_to_test,flights_to_test


class TestBookings:

    @pytest.mark.parametrize("passenger_case", passengers_to_test)
    def test_create_booking_passenger_validation(self,create_booking_passenger_case,passenger_case):
        response = create_booking_passenger_case(passenger_case["passengers"])
        assert response.status_code == passenger_case["expected_status"]

    @pytest.mark.parametrize("flight_case", flights_to_test)
    def test_create_booking_flight_validation(self,create_booking_flight_case,flight_case):
        response = create_booking_flight_case(flight_case["flight_id"])
        assert response.status_code == flight_case["expected_status"]


