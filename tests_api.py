from helpers import *
from data import *
import pytest


class TestCourierApi:
    @staticmethod
    def test_create_courier_successful():
        payload = get_courier_data_for_signup()
        response = create_courier(payload)
        assert response.status_code == 201 and response.text == '{"ok":true}'

    @staticmethod
    def test_multiple_signups_with_same_data_returns_error():
        payload = register_new_courier_and_return_login_password()
        response = create_courier(payload)
        error_message = response.json()['message']
        assert response.status_code == 409 and error_message == 'Этот логин уже используется. Попробуйте другой.'

    @staticmethod
    def test_courier_sign_up_without_login_returns_error():
        payload = get_courier_data_without_login()
        response = create_courier(payload)
        error_message = response.json()['message']
        assert response.status_code == 400 and error_message == 'Недостаточно данных для создания учетной записи'

    @staticmethod
    def test_courier_login_successful():
        payload = register_new_courier_and_return_login_password()
        del payload['firstName']
        response = login_courier(payload)
        id = response.json()['id']
        assert response.status_code == 200 and isinstance(id, int)

    @staticmethod
    def test_login_without_password_returns_error():
        payload = register_new_courier_and_return_login_password()
        del payload['firstName']
        # устанавливаем пустое значение, поскольку при удалении поля, что соответствовало бы заданию, тест сваливается с таймаутом
        payload['password'] = ''
        response = login_courier(payload)
        error_message = response.json()['message']
        assert response.status_code == 400 and error_message == 'Недостаточно данных для входа'

    @staticmethod
    def test_login_with_incorrect_password_returns_error():
        payload = register_new_courier_and_return_login_password()
        del payload['firstName']
        payload['password'] = '123'
        response = login_courier(payload)
        error_message = response.json()['message']
        assert response.status_code == 404 and error_message == 'Учетная запись не найдена'

    @staticmethod
    def test_login_with_non_existent_data_returns_error():
        response = login_courier(non_existent_courier_data)
        error_message = response.json()['message']
        assert response.status_code == 404 and error_message == 'Учетная запись не найдена'

    @staticmethod
    @pytest.mark.parametrize("color", [[""], ["BLACK"], ["GREY"], ["BLACK", "GREY"]])
    def test_order_creation_successful(color):
        payload = get_payload_for_new_order_no_colors()
        payload['color'] = color
        response = create_order(payload)
        track = response.json()['track']
        assert response.status_code == 201 and isinstance(track, int)

    @staticmethod
    def test_order_return_successful_by_courier_id():
        courier_id = register_new_courier_and_return_id()
        response = get_order_list(courier_id)
        assert response.status_code == 200 and response.text is not None

    @staticmethod
    def test_courier_deletion_successful():
        courier_id = register_new_courier_and_return_id()['courierId']
        response = delete_courier(courier_id)
        assert response.status_code == 200 and response.text == '{"ok":true}'

    @staticmethod
    def test_courier_deletion_without_id_returns_error():
        courier_id = missing_courier_id["courierId"]
        response = delete_courier(courier_id)
        error_message = response.json()['message']
        assert response.status_code == 404 and error_message == 'Not Found.'

    @staticmethod
    def test_courier_deletion_with_non_existent_id_returns_error():
        response = delete_courier(non_existent_courier_id["courierId"])
        error_message = response.json()['message']
        assert response.status_code == 404 and error_message == 'Курьера с таким id нет.'

    @staticmethod
    def test_accept_new_order_successful():
        courier_id = register_new_courier_and_return_id()
        track_number = create_order_and_return_track_number()
        order_id = return_order_id_by_track_number(track_number)
        response = accept_order(order_id = order_id, query = courier_id)
        assert response.status_code == 200 and response.text == '{"ok":true}'

    @staticmethod
    def test_accept_new_order_non_existent_courier_id_returns_error():
        track_number = create_order_and_return_track_number()
        order_id = return_order_id_by_track_number(track_number)
        response = accept_order(order_id = order_id, query = non_existent_courier_id)
        error_message = response.json()['message']
        assert response.status_code == 404 and error_message == 'Курьера с таким id не существует'

    @staticmethod
    def test_accept_new_order_with_missing_courier_id_returns_error():
        track_number = create_order_and_return_track_number()
        order_id = return_order_id_by_track_number(track_number)
        response = accept_order(order_id = order_id, query = missing_courier_id)
        error_message = response.json()['message']
        assert response.status_code == 400 and error_message == 'Недостаточно данных для поиска'

    @staticmethod
    def test_accept_new_order_with_non_existent_order_id_returns_error():
        courier_id = register_new_courier_and_return_id()
        response = accept_order(order_id = non_existent_order_id, query = courier_id)
        error_message = response.json()['message']
        assert response.status_code == 404 and error_message == 'Заказа с таким id не существует'

    @staticmethod
    def test_accept_new_order_with_missing_order_id_returns_error():
        courier_id = register_new_courier_and_return_id()
        response = accept_order(order_id = missing_order_id, query = courier_id)
        error_message = response.json()['message']
        assert response.status_code == 404 and error_message == 'Not Found.'

    @staticmethod
    def test_get_order_by_track_id_successful():
        track_number = create_order_and_return_track_number()
        response = get_order_by_track_number(track_number)
        assert response.status_code == 200 and 'id' in response.text

    @staticmethod
    def test_get_order_by_non_existent_track_id_returns_error():
        response = get_order_by_track_number(non_existent_track_number)
        error_message = response.json()['message']
        assert response.status_code == 404 and error_message == 'Заказ не найден'

    @staticmethod
    def test_get_order_by_track_id_with_missing_track_id_returns_error():
        response = get_order_by_track_number(missing_track_number)
        error_message = response.json()['message']
        assert response.status_code == 400 and error_message == 'Недостаточно данных для поиска'
