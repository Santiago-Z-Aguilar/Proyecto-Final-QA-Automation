from datetime import datetime, timedelta
from API.utils.data import *

# ---------- POST DATA ----------

data_post_success = {
    "origin": valid_iata_origin,
    "destination": valid_iata_destination,
    "departure_time": datetime_today,
    "arrival_time": datetime_future,
    "base_price": base_price_valid,
    "aircraft_id": ""
}

data_post_invalid_origin = {
    "origin": iata_four_chr ,
    "destination": valid_iata_destination,
    "departure_time": datetime_today,
    "arrival_time": datetime_future,
    "base_price": base_price_valid,
    "aircraft_id": ""
}

data_post_origin_empty = {
    "origin": iata_empty,
    "destination": valid_iata_destination,
    "departure_time": datetime_today,
    "arrival_time": datetime_future,
    "base_price": base_price_valid,
    "aircraft_id": ""
}

data_post_origin_none = {
    "origin": None,
    "destination": valid_iata_destination,
    "departure_time": datetime_today,
    "arrival_time": datetime_future,
    "base_price": base_price_valid,
    "aircraft_id": ""
}

data_post_destination_invalid = {
    "origin": valid_iata_origin,
    "destination": iata_number_letters,
    "departure_time": datetime_today,
    "arrival_time": datetime_future,
    "base_price": base_price_valid,
    "aircraft_id": ""
}

data_post_origin_dest_same = {
    "origin": valid_iata_origin,
    "destination": valid_iata_origin,
    "departure_time": datetime_today,
    "arrival_time": datetime_today,
    "base_price": base_price_valid,
    "aircraft_id": ""
}

data_post_departure_in_past = {
    "origin": valid_iata_origin,
    "destination": valid_iata_destination,
    "departure_time": datetime_today,
    "arrival_time": datetime_pass,
    "base_price": base_price_valid,
    "aircraft_id": ""
}

data_post_negative_price = {
    "origin": valid_iata_origin,
    "destination": valid_iata_destination,
    "departure_time": datetime_today,
    "arrival_time": datetime_future,
    "base_price": base_price_negative,
    "aircraft_id": ""
}

data_post_zero_price = {
    "origin": valid_iata_origin,
    "destination": valid_iata_destination,
    "departure_time": datetime_today,
    "arrival_time": datetime_future,
    "base_price": base_price_zero,
    "aircraft_id": ""
}

data_post_nonumeric_price = {
    "origin": valid_iata_origin,
    "destination": valid_iata_destination,
    "departure_time": datetime_today,
    "arrival_time": datetime_future,
    "base_price": base_price_string,
    "aircraft_id": ""
}

data_post_int_price = {
    "origin": valid_iata_origin,
    "destination": valid_iata_destination,
    "departure_time": datetime_today,
    "arrival_time": datetime_future,
    "base_price": base_price_int,
    "aircraft_id": ""
}

data_post_30digits_price = {
    "origin": valid_iata_origin,
    "destination": valid_iata_destination,
    "departure_time": datetime_today,
    "arrival_time": datetime_future,
    "base_price": base_price_30digits,
    "aircraft_id": ""
}

data_post_nonexistent_aircraft = {
    "origin": valid_iata_origin,
    "destination": valid_iata_destination,
    "departure_time": datetime_today,
    "arrival_time": datetime_future,
    "base_price": base_price_valid,
    "aircraft_id": id_aircraft_generated
}

data_post_empty_aircraft = {
    "origin": valid_iata_origin,
    "destination": valid_iata_destination,
    "departure_time": datetime_today,
    "arrival_time": datetime_future,
    "base_price": base_price_valid,
    "aircraft_id": id_aircraft_empty
}

data_post_number_aircraft = {
    "origin": valid_iata_origin,
    "destination": valid_iata_destination,
    "departure_time": datetime_today,
    "arrival_time": datetime_future,
    "base_price": base_price_valid,
    "aircraft_id": id_aircraft_number
}

data_post_fields_missing = {
    "destination": "valid_iata_destination",
    "departure_time": datetime_today,
    "arrival_time": datetime_future,
    "aircraft_id": ""
}

data_post_json_disarray = {
    "departure_time": datetime_today,
    "arrival_time": datetime_future,
    "base_price": base_price_valid,
    "origin": valid_iata_origin,
    "destination": valid_iata_destination,
    "aircraft_id": ""
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
    "origin": valid_iata_origin,
    "destination": valid_iata_destination,
    "departure_time": datetime_today,
    "arrival_time": datetime_future,
    "base_price": base_price_valid,
    "aircraft_id": ""
}

data_put_invalid_origin = {
    "origin": iata_lowercase,
    "destination": valid_iata_destination,
    "departure_time": datetime_today,
    "arrival_time": datetime_future,
    "base_price": base_price_valid,
    "aircraft_id": ""
}


data_put_invalid_destination = {
    "origin": valid_iata_origin,
    "destination": iata_number_letters,
    "departure_time": datetime_today,
    "arrival_time": datetime_future,
    "base_price": base_price_valid,
    "aircraft_id": ""
}

data_put_arrival_before_dep = {
    "origin": valid_iata_origin,
    "destination": valid_iata_destination,
    "departure_time": datetime_today,
    "arrival_time": datetime_pass,
    "base_price": base_price_valid,
    "aircraft_id": ""
}

data_put_zero_price = {
    "origin": valid_iata_origin,
    "destination": valid_iata_destination,
    "departure_time": datetime_today,
    "arrival_time": datetime_future,
    "base_price": base_price_zero,
    "aircraft_id": ""
}

data_put_negative_price = {
    "origin": valid_iata_origin,
    "destination": valid_iata_destination,
    "departure_time": datetime_today,
    "arrival_time": datetime_future,
    "base_price": base_price_negative,
    "aircraft_id": ""
}

data_put_float_price = {
    "origin": valid_iata_origin,
    "destination": valid_iata_destination,
    "departure_time": datetime_today,
    "arrival_time": datetime_future,
    "base_price": base_price_valid,
    "aircraft_id": ""
}

data_put_price_30digits = {
    "origin": valid_iata_origin,
    "destination": valid_iata_destination,
    "departure_time": datetime_today,
    "arrival_time": datetime_future,
    "base_price": base_price_30digits,
    "aircraft_id": ""
}

