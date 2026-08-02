from endpoint_executions import *
import pytest
import allure
from helpers import DataGeneration

class TestOrderCreation:
    @allure.title('Проверка успешного создания заказа с разными цветами самоката')
    @pytest.mark.parametrize("color", [[""], ["BLACK"], ["GREY"], ["BLACK", "GREY"]])
    def test_order_creation_successful(self, color):
        payload = DataGeneration().get_payload_for_new_order_no_colors()
        payload['color'] = color
        response = create_order(payload)
        track = response.json()['track']
        assert response.status_code == 201 and isinstance(track, int)
