from datetime import datetime, timedelta

# ---------- POST DATA ----------

data_post_success = {
    "origin": "NAA",
    "destination": "VQW",
    "departure_time": "2025-08-17T23:58:27.212Z",
    "arrival_time": "2025-08-17T23:58:27.212Z",
    "base_price": 0,
    "aircraft_id": "acf-85527eba"
}

data_post_invalid_origin = {
    "origin": "VREY",
    "destination": "BXH",
    "departure_time": "2025-08-17T23:58:27.212Z",
    "arrival_time": "2025-08-18T15:57:27.212Z",
    "base_price": 100,
    "aircraft_id": "acf-736dd0f9"
}

data_post_origin_empty = {
    "origin": "",
    "destination": "BXH",
    "departure_time": "2025-08-17T23:58:27.212Z",
    "arrival_time": "2025-08-18T15:57:27.212Z",
    "base_price": 100,
    "aircraft_id": "acf-736dd0f9"
}

data_post_destination_invalid = {
    "origin": "BUE",
    "destination": "AAAA",
    "departure_time": "2025-08-17T23:58:27.212Z",
    "arrival_time": "2025-08-18T15:57:27.212Z",
    "base_price": 100,
    "aircraft_id": "acf-736dd0f9"
}

data_post_origin_null = {
    "origin": None,
    "destination": "AAAA",
    "departure_time": "2025-08-17T23:58:27.212Z",
    "arrival_time": "2025-08-18T15:57:27.212Z",
    "base_price": 100,
    "aircraft_id": "acf-736dd0f9"
}

data_post_origin_dest_same = {
    "origin": "BUE",
    "destination": "BUE",
    "departure_time": "2025-08-17T23:58:27.212Z",
    "arrival_time": "2025-08-18T15:57:27.212Z",
    "base_price": 100,
    "aircraft_id": "acf-736dd0f9"
}

def data_post_departure_in_past():
    yesterday = (datetime.utcnow() - timedelta(days=1)).isoformat() + "Z"
    arrival = (datetime.utcnow() + timedelta(days=1)).isoformat() + "Z"
    return {
        "origin": "BUE",
        "destination": "XFA",
        "departure_time": yesterday,
        "arrival_time": arrival,
        "base_price": 100,
        "aircraft_id": "acf-736dd0f9"
    }

data_post_negative_price = {
    "origin": "BUE",
    "destination": "XFA",
    "departure_time": "2025-10-17T23:58:27.212Z",
    "arrival_time": "2025-12-18T15:57:27.212Z",
    "base_price": -50,
    "aircraft_id": "acf-736dd0f9"
}

data_post_zero_price = {
    "origin": "BUE",
    "destination": "XFA",
    "departure_time": "2025-10-17T23:58:27.212Z",
    "arrival_time": "2025-12-18T15:57:27.212Z",
    "base_price": 0,
    "aircraft_id": "acf-736dd0f9"
}

data_post_nonumeric_price = {
    "origin": "BUE",
    "destination": "XFA",
    "departure_time": "2025-10-17T23:58:27.212Z",
    "arrival_time": "2025-12-18T15:57:27.212Z",
    "base_price": "ten",
    "aircraft_id": "acf-736dd0f9"
}

data_post_nonexistent_aircraft = {
    "origin": "BUE",
    "destination": "XFA",
    "departure_time": "2025-10-17T23:58:27.212Z",
    "arrival_time": "2025-12-18T15:57:27.212Z",
    "base_price": 200,
    "aircraft_id": "acf-736zz8f9"
}

data_post_empty_aircraft = {
    "origin": "BUE",
    "destination": "XFA",
    "departure_time": "2025-10-17T23:58:27.212Z",
    "arrival_time": "2025-12-18T15:57:27.212Z",
    "base_price": 200,
    "aircraft_id": ""
}

data_post_fields_missing = {
    "destination": "XFA",
    "departure_time": "2025-10-17T23:58:27.212Z",
    "arrival_time": "2025-12-18T15:57:27.212Z",
    "aircraft_id": ""
}

data_post_json_disarray = {
    "departure_time": "2025-10-17T23:58:27.212Z",
    "arrival_time": "2025-12-18T15:57:27.212Z",
    "base_price": 200,
    "origin": "BUE",
    "destination": "XFA",
    "aircraft_id": "acf-d8c34ac1"
}

data_post_repetitive = {
    "origin": "QBZ",
    "destination": "FTN",
    "departure_time": "2025-08-20T23:43:49.341Z",
    "arrival_time": "2025-08-21T00:43:49.341Z",
    "base_price": 300,
    "aircraft_id": "acf-1890ddf3"
}

# ---------- PUT DATA ----------

data_put_valid = {
    "origin": "BUE",
    "destination": "MIA",
    "departure_time": "2025-11-01T10:00:00.000Z",
    "arrival_time": "2025-11-01T15:00:00.000Z",
    "base_price": 300,
    "aircraft_id": "acf-d8c34ac1"
}

data_put_invalid_origin = {
    "origin": "DE8",
    "destination": "SCP",
    "departure_time": "2026-01-20T23:43:49.341Z",
    "arrival_time": "2026-01-21T03:43:49.341Z",
    "base_price": 700,
    "aircraft_id": "acf-a39c2435"
}

data_put_invalid_destination = {
    "origin": "DEU",
    "destination": "SC5",
    "departure_time": "2026-01-20T23:43:49.341Z",
    "arrival_time": "2026-01-21T03:43:49.341Z",
    "base_price": 700,
    "aircraft_id": "acf-a39c2435"
}

data_put_arrival_before_dep = {
    "origin": "DEU",
    "destination": "SCP",
    "departure_time": "2026-02-20T23:43:49.341Z",
    "arrival_time": "2026-01-21T03:43:49.341Z",
    "base_price": 700.00,
    "aircraft_id": "acf-a39c2435"
}

data_put_zero_price = {
    "origin": "DEU",
    "destination": "SCP",
    "departure_time": "2026-01-20T23:43:49.341Z",
    "arrival_time": "2026-01-21T03:43:49.341Z",
    "base_price": 0,
    "aircraft_id": "acf-a39c2435"
}

data_put_negative_price = {
    "origin": "DEU",
    "destination": "SCP",
    "departure_time": "2026-01-20T23:43:49.341Z",
    "arrival_time": "2026-01-21T03:43:49.341Z",
    "base_price": -100,
    "aircraft_id": "acf-a39c2435"
}

data_put_float_price = {
    "origin": "DEU",
    "destination": "SCP",
    "departure_time": "2026-01-20T23:43:49.341Z",
    "arrival_time": "2026-01-21T03:43:49.341Z",
    "base_price": 200.48,
    "aircraft_id": "acf-a39c2435"
}

data_put_float_price_nolimit = {
    "origin": "DEU",
    "destination": "SCP",
    "departure_time": "2026-01-20T23:43:49.341Z",
    "arrival_time": "2026-01-21T03:43:49.341Z",
    "base_price": 200.4888888888888888888888,
    "aircraft_id": "acf-a39c2435"
}

data_put_nonexistent_flight = {
    "origin": "DEU",
    "destination": "SCP",
    "departure_time": "2026-01-20T23:43:49.341Z",
    "arrival_time": "2026-01-21T03:43:49.341Z",
    "base_price": 200.00,
    "aircraft_id": "acf-a39c243"
}
