import random
import string
import allure

class DataGeneration:
    def generate_random_string(self, length: int) -> str:
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    def generate_random_int(self, length: int) -> str:
        digits = string.digits
        random_int = ''.join(random.choice(digits) for i in range(length))
        return random_int

    def generate_login(self, length: int) -> str:
        return self.generate_random_string(length)

    def generate_pass(self, length: int) -> str:
        return self.generate_random_string(length)

    def generate_first_name(self, length: int) -> str:
        return self.generate_random_string(length)

    def generate_last_name(self, length: int) -> str:
        return self.generate_random_string(length)

    def generate_address(self, length: int) -> str:
        return self.generate_random_string(length)

    def generate_metro_station(self, length: int) -> str:
        return self.generate_random_int(length)

    def generate_phone(self, length: int) -> str:
        return f'+7{self.generate_random_int(length)}'

    def generate_rent_time(self, length: int) -> str:
        return self.generate_random_int(length)

    def generate_comment(self, length: int) -> str:
        return self.generate_random_string(length)

    def generate_date(self) -> str:
        dates = [
            '2026-06-30',
            '2026-07-30',
            '2026-08-30',
            '2026-09-30',
            '2026-10-30',
        ]
        return random.choice(dates)

    @allure.step('Создаем данные курьера для регистрации')
    def get_courier_data_for_signup(self) -> dict:
        courier_data = {
            "login": self.generate_login(5),
            "password": self.generate_pass(5),
            "firstName": self.generate_first_name(5),
        }
        return courier_data

    @allure.step('Создаем невалидные данные курьера для регистрации без имени логина')
    def get_courier_data_without_login(self) -> dict:
        courier_data = {
            "password": self.generate_pass(5),
            "firstName": self.generate_first_name(5),
        }
        return courier_data

    @allure.step('Создаем данные заказа')
    def get_payload_for_new_order_no_colors(self) -> dict:
        payload = {
            "firstName": self.generate_first_name(5),
            "lastName": self.generate_first_name(5),
            "address": self.generate_address(5),
            "metroStation": self.generate_metro_station(1),
            "phone": self.generate_phone(10),
            "rentTime": self.generate_rent_time(1),
            "deliveryDate": self.generate_date(),
            "comment": self.generate_comment(5)
        }
        return payload
