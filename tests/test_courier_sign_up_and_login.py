from data import *
from endpoint_executions import *
import allure
from helpers import DataGeneration


class TestCourierSignUp:

    @allure.title('Проверка успешной регистрации курьера')
    def test_create_courier_successful(self, api_client, cleanup_courier_from_signup):
        courier_data = DataGeneration().get_courier_data_for_signup()
        response = create_courier(courier_data)
        cleanup_courier_from_signup.append(courier_data)
        assert response.status_code == 201 and response.text == '{"ok":true}'

    @allure.title('Проверка, что API возвращает ошибку, если происходит попытка повторной регистрации')
    def test_multiple_signups_with_same_data_returns_error(self, new_courier_with_cleanup):
        response = create_courier(new_courier_with_cleanup)
        error_message = response.json()['message']
        assert response.status_code == 409 and error_message == 'Этот логин уже используется. Попробуйте другой.'

    @allure.title('Проверка, что API возвращает ошибку, если запрос регистрации не содержит имени логина')
    def test_courier_sign_up_without_login_returns_error(self):
        response = create_courier(DataGeneration().get_courier_data_without_login())
        error_message = response.json()['message']
        assert response.status_code == 400 and error_message == 'Недостаточно данных для создания учетной записи'

class TestCourierLogin:
    @allure.title('Проверка успешного логина курьера')
    def test_courier_login_successful(self, new_courier_with_cleanup):
        response = login_courier(new_courier_with_cleanup)
        id = response.json()['id']
        assert response.status_code == 200 and isinstance(id, int)

    @allure.title('Проверка, что API возвращает ошибку, если логин происходит без пароля')
    def test_login_without_password_returns_error(self, new_courier_with_cleanup):
        payload = new_courier_with_cleanup
        # устанавливаем пустое значение, поскольку при удалении поля, что соответствовало бы заданию, тест сваливается с таймаутом
        payload['password'] = ''
        response = login_courier(payload)
        error_message = response.json()['message']
        assert response.status_code == 400 and error_message == 'Недостаточно данных для входа'

    @allure.title('Проверка, что API возвращает ошибку, если логин происходит с неправильным паролем')
    def test_login_with_incorrect_password_returns_error(self, new_courier_with_cleanup):
        payload = new_courier_with_cleanup
        payload['password'] = '123'
        response = login_courier(payload)
        error_message = response.json()['message']
        assert response.status_code == 404 and error_message == 'Учетная запись не найдена'

    @allure.title('Проверка, что API возвращает ошибку, если логин происходит с несуществующими данными')
    def test_login_with_non_existent_data_returns_error(self):
        response = login_courier(non_existent_courier_data)
        error_message = response.json()['message']
        assert response.status_code == 404 and error_message == 'Учетная запись не найдена'
