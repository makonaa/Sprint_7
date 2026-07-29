import random
import string
from endpoint_executions import *

def generate_random_string(length: int) -> str:
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string

def generate_random_int(length: int) -> str:
    digits = string.digits
    random_int = ''.join(random.choice(digits) for i in range(length))
    return random_int

def generate_login(length: int) -> str:
    return generate_random_string(length)

def generate_pass(length: int) -> str:
    return generate_random_string(length)

def generate_first_name(length: int) -> str:
    return generate_random_string(length)

def generate_last_name(length: int) -> str:
    return generate_random_string(length)

def generate_address(length: int) -> str:
    return generate_random_string(length)

def generate_metro_station(length: int) -> str:
    return generate_random_int(length)

def generate_phone(length: int) -> str:
    return f'+7{generate_random_int(length)}'

def generate_rent_time(length: int) -> str:
    return generate_random_int(length)

def generate_comment(length: int) -> str:
    return generate_random_string(length)

def generate_date() -> str:
    dates = [
        '2026-06-30',
        '2026-07-30',
        '2026-08-30',
        '2026-09-30',
        '2026-10-30',
    ]
    return random.choice(dates)

def get_courier_data_for_signup() -> dict:
    courier_data = {
        "login": generate_login(5),
        "password": generate_pass(5),
        "firstName": generate_first_name(5),
    }
    return courier_data

def get_courier_data_without_login() -> dict:
    courier_data = {
        "password": generate_pass(5),
        "firstName": generate_first_name(5),
    }
    return courier_data

def register_new_courier_and_return_login_password() -> dict:
    payload = get_courier_data_for_signup()
    response = create_courier(payload)
    if response.status_code == 201:
        return payload
    else:
        raise Exception("Failed to register new courier")

def register_new_courier_and_return_id() -> dict:
    payload = get_courier_data_for_signup()
    response = create_courier(payload)
    if response.status_code == 201:
        response_with_id = login_courier(payload)
        if response_with_id.status_code == 200:
            courier_id = {
                "courierId": response_with_id.json()['id']
            }
            return courier_id
        else:
            raise Exception("Failed to login with existing courier")
    else:
        raise Exception("Failed to register new courier")

def get_payload_for_new_order_no_colors() -> dict:
    payload = {
        "firstName": generate_first_name(5),
        "lastName": generate_first_name(5),
        "address": generate_address(5),
        "metroStation": generate_metro_station(1),
        "phone": generate_phone(10),
        "rentTime": generate_rent_time(1),
        "deliveryDate": generate_date(),
        "comment": generate_comment(5)
    }
    return payload

def create_order_and_return_track_number() -> dict:
    payload = get_payload_for_new_order_no_colors()
    response = create_order(payload)
    if response.status_code == 201:
        track = {
            "t": response.json()['track']
        }
        return track
    else:
        raise Exception("Failed to create new order")

def return_order_id_by_track_number(query:dict) -> int:
    response = get_order_by_track_number(query)
    if response.status_code == 200:
        order_id = response.json()['order']['id']
        return order_id
    else:
        raise Exception('Failed to get order id by track number')
