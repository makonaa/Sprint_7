from data import *
from endpoint_executions import *
import allure


class TestCourierDeletion:
    @allure.title('Проверка, что курьер успешно удаляется')
    def test_courier_deletion_successful(self, courier_id):
        response = delete_courier(courier_id["courierId"])
        assert response.status_code == 200 and response.text == '{"ok":true}'

    @allure.title('Проверка, что API возвращает ошибку, если удаление происходит без id курьера')
    def test_courier_deletion_without_id_returns_error(self):
        courier_id = missing_courier_id["courierId"]
        response = delete_courier(courier_id)
        error_message = response.json()['message']
        assert response.status_code == 404 and error_message == 'Not Found.'

    @allure.title('Проверка, что API возвращает ошибку, если удаление происходит с несуществующим id курьера')
    def test_courier_deletion_with_non_existent_id_returns_error(self):
        response = delete_courier(non_existent_courier_id["courierId"])
        error_message = response.json()['message']
        assert response.status_code == 404 and error_message == 'Курьера с таким id нет.'
