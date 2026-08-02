import pytest
from endpoint_executions import *
from api_client import ApiClient
import allure

@pytest.fixture
def api_client():
    return ApiClient()

@pytest.fixture
def new_courier(api_client):
    return api_client.register_new_courier_and_return_login_password()

@pytest.fixture
def courier_id(new_courier, api_client):
    return api_client.return_id_for_registered_courier(new_courier)

@pytest.fixture
def new_courier_with_cleanup(new_courier, courier_id):
    yield new_courier
    courier_id_to_delete = courier_id['courierId']
    try:
        delete_courier(courier_id_to_delete)
    except Exception as ex:
        message = f'Failed to delete courier with id: {courier_id}, error: {ex}'
        allure.attach(message, name='Error during cleanup', attachment_type=allure.attachment_type.TEXT)

@pytest.fixture
def courier_id_with_cleanup(courier_id):
    yield courier_id
    courier_id_to_delete = courier_id['courierId']
    try:
        delete_courier(courier_id_to_delete)
    except Exception as ex:
        message = f'Failed to delete courier with id: {courier_id}, error: {ex}'
        allure.attach(message, name='Error during cleanup', attachment_type=allure.attachment_type.TEXT)

@pytest.fixture
def cleanup_courier_from_signup(api_client):
    list_to_cleanup = []
    yield list_to_cleanup
    for item in list_to_cleanup:
        courier_id = api_client.return_id_for_registered_courier(item)
        delete_courier(courier_id['courierId'])
