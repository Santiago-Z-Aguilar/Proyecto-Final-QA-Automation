import os
import pytest
from jsonschema import validate


class TestAircrafts:
    def test_create_aircraft(self,create_aircraft):
        response = create_aircraft
        assert response.status_code == 201
