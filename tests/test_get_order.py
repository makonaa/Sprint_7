from data import *
from endpoint_executions import *
import allure


class TestGetOrder:
    @allure.title('Проверка успешного получения заказа по его трек-номеру')
    def test_get_order_by_track_id_successful(self, api_client):
        track_number = api_client.create_order_and_return_track_number()
        response = get_order_by_track_number(track_number)
        assert response.status_code == 200 and 'id' in response.text

    @allure.title('Проверка, что API возвращает ошибку, если предоставленный трек-номер не существует')
    def test_get_order_by_non_existent_track_id_returns_error(self):
        response = get_order_by_track_number(non_existent_track_number)
        error_message = response.json()['message']
        assert response.status_code == 404 and error_message == 'Заказ не найден'

    @allure.title('Проверка, что API возвращает ошибку, если трек-номер не предоставлен')
    def test_get_order_by_track_id_with_missing_track_id_returns_error(self):
        response = get_order_by_track_number(missing_track_number)
        error_message = response.json()['message']
        assert response.status_code == 400 and error_message == 'Недостаточно данных для поиска'
