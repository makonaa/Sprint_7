from endpoint_list import *
import requests

def create_courier(payload:dict) -> requests.Response:
    return requests.post(CREATE_COURIER_URL, data=payload)

def login_courier(payload:dict) -> requests.Response:
    return requests.post(LOGIN_COURIER_URL, data=payload)

def create_order(payload:dict) -> requests.Response:
    return requests.post(CREATE_ORDER_URL, json=payload)

def get_order_list(query:dict) -> requests.Response:
    return requests.get(GET_ORDER_LIST_URL, params=query)

def delete_courier(courier_id:int) -> requests.Response:
    return requests.delete(DELETE_COURIER_URL.format(courier_id=courier_id))

def get_order_by_track_number(query: dict) -> requests.Response:
    return requests.get(GET_ORDER_BY_TRACK_NUMBER_URL, params=query)

def accept_order(order_id:int, query:dict) -> requests.Response:
    return requests.put(ACCEPT_ORDER_URL.format(order_id=order_id), params=query)
