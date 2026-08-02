from endpoint_executions import *
import allure

class TestGetOrderList:
    @allure.title('Проверка успешного получения списка заказов по id курьера')
    def test_order_return_successful_by_courier_id(self, courier_id_with_cleanup):
        response = get_order_list(courier_id_with_cleanup)
        assert response.status_code == 200 and response.text is not None
