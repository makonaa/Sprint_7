from data import *
from endpoint_executions import *
import allure

class TestAcceptNewOrder:

    @allure.title('Проверка успешного принятия нового заказа')
    def test_accept_new_order_successful(self, courier_id_with_cleanup, api_client):
        track_number = api_client.create_order_and_return_track_number()
        order_id = api_client.return_order_id_by_track_number(track_number)
        response = accept_order(order_id = order_id, query = courier_id_with_cleanup)
        assert response.status_code == 200 and response.text == '{"ok":true}'

    @allure.title('Проверка, что API возвращает ошибку, если заказ принимается с несуществующим id курьера')
    def test_accept_new_order_non_existent_courier_id_returns_error(self, api_client):
        track_number = api_client.create_order_and_return_track_number()
        order_id = api_client.return_order_id_by_track_number(track_number)
        response = accept_order(order_id = order_id, query = non_existent_courier_id)
        error_message = response.json()['message']
        assert response.status_code == 404 and error_message == 'Курьера с таким id не существует'

    @allure.title('Проверка, что API возвращает ошибку, если заказ принимается без id курьера')
    def test_accept_new_order_with_missing_courier_id_returns_error(self, api_client):
        track_number = api_client.create_order_and_return_track_number()
        order_id = api_client.return_order_id_by_track_number(track_number)
        response = accept_order(order_id = order_id, query = missing_courier_id)
        error_message = response.json()['message']
        assert response.status_code == 400 and error_message == 'Недостаточно данных для поиска'

    @allure.title('Проверка, что API возвращает ошибку, если заказ принимается с несуществующим id заказа')
    def test_accept_new_order_with_non_existent_order_id_returns_error(self, courier_id_with_cleanup):
        response = accept_order(order_id = non_existent_order_id, query = courier_id_with_cleanup)
        error_message = response.json()['message']
        assert response.status_code == 404 and error_message == 'Заказа с таким id не существует'

    @allure.title('Проверка, что API возвращает ошибку, если заказ принимается без id заказа')
    def test_accept_new_order_with_missing_order_id_returns_error(self, courier_id_with_cleanup):
        response = accept_order(order_id = missing_order_id, query = courier_id_with_cleanup)
        error_message = response.json()['message']
        assert response.status_code == 404 and error_message == 'Not Found.'
