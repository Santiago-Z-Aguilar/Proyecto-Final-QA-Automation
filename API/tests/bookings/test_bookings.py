import pytest
from API.utils.data import


class TestBookings:
    def test_create_booking(self,create_booking):
        response = create_booking
        assert response.status_code == 201

