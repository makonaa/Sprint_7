from endpoint_list import *
import requests
import allure

@allure.step('Регистрируем курьера')
def create_courier(payload:dict) -> requests.Response:
    return requests.post(CREATE_COURIER_URL, data=payload)

@allure.step('Выполняем логин зарегистрированным курьером')
def login_courier(payload:dict) -> requests.Response:
    return requests.post(LOGIN_COURIER_URL, data=payload)

@allure.step('Создаем новый заказ')
def create_order(payload:dict) -> requests.Response:
    return requests.post(CREATE_ORDER_URL, json=payload)

@allure.step('Получаем список заказов курьера')
def get_order_list(query:dict) -> requests.Response:
    return requests.get(GET_ORDER_LIST_URL, params=query)

@allure.step('Удаляем курьера')
def delete_courier(courier_id:int) -> requests.Response:
    return requests.delete(DELETE_COURIER_URL.format(courier_id=courier_id))

@allure.step('Получаем заказ по его трек-номеру')
def get_order_by_track_number(query: dict) -> requests.Response:
    return requests.get(GET_ORDER_BY_TRACK_NUMBER_URL, params=query)

@allure.step('Принимаем заказ курьером')
def accept_order(order_id:int, query:dict) -> requests.Response:
    return requests.put(ACCEPT_ORDER_URL.format(order_id=order_id), params=query)
