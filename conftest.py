import pytest
from helpers import DataGeneration
from endpoint_executions import *
from api_client import ApiClient

@pytest.fixture
def get_courier_data():
    return DataGeneration().get_courier_data_for_signup()

@pytest.fixture
def get_courier_data_without_login():
    return DataGeneration().get_courier_data_without_login()

@pytest.fixture
def get_payload_for_new_order():
    return DataGeneration().get_payload_for_new_order_no_colors()

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
        print(f'Failed to delete courier with id: {courier_id}, error: {ex}')

@pytest.fixture
def courier_id_with_cleanup(courier_id):
    yield courier_id
    courier_id_to_delete = courier_id['courierId']
    try:
        delete_courier(courier_id_to_delete)
    except Exception as ex:
        print(f'Failed to delete courier with id: {courier_id}, error: {ex}')
