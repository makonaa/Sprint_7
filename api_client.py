from endpoint_executions import *
from helpers import DataGeneration
import allure
from custom_exceptions import *

class ApiClient:
    def __init__(self):
        self.data = DataGeneration()

    @allure.step('Создаем зарегистрированного курьера и возвращаем его логин/пароль')
    def register_new_courier_and_return_login_password(self) -> dict:
        payload = self.data.get_courier_data_for_signup()
        response = create_courier(payload)
        if response.status_code == 201:
            del payload['firstName']
            return payload
        else:
            raise FailedToRegisterCourier(
                "Failed to register new courier"
                f'Error code: {response.status_code}, payload: {response.text}'
            )

    @allure.step('Возвращаем id уже зарегистрированного курьера')
    def return_id_for_registered_courier(self, courier_data: dict) -> dict:
        response_with_id = login_courier(courier_data)
        if response_with_id.status_code == 200:
            courier_id = {
                "courierId": response_with_id.json()['id']
            }
            return courier_id
        else:
            raise FailedToLoginCourier(
                "Failed to login with existing courier"
                f'Error code: {response_with_id.status_code}, payload: {response_with_id.text}'
            )

    @allure.step('Создаем новый заказ и возвращаем его трек-номер')
    def create_order_and_return_track_number(self) -> dict:
        payload = self.data.get_payload_for_new_order_no_colors()
        response = create_order(payload)
        if response.status_code == 201:
            track = {
                "t": response.json()['track']
            }
            return track
        else:
            raise FailedToCreateOrder(
                "Failed to create new order"
                f'Error code: {response.status_code}, payload: {response.text}'
            )

    @allure.step('Возвращаем id заказа по его трек-номеру')
    def return_order_id_by_track_number(self, query: dict) -> int:
        response = get_order_by_track_number(query)
        if response.status_code == 200:
            order_id = response.json()['order']['id']
            return order_id
        else:
            raise FailedToGetOrderId(
                'Failed to get order id by track number'
                f'Error code: {response.status_code}, payload: {response.text}'
            )
