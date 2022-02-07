import json
from werkzeug.security import generate_password_hash

from faker import Faker

faker = Faker('ru-RU')


def create_fake_users(count):
    json_list = []  # список словарей для сохранения в файл json
    for i in range(count):
        users_info = {
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "age": faker.random_int(20, 90),
            "nickname": faker.user_name(),
            "password": generate_password_hash(faker.password()),
            "email": faker.email(),
            "description": faker.text(90),
            "is_admin": False,
            "last_login": f'{faker.date_time_this_year()}',
        }
        json_list.append(users_info)
    return json_list


if __name__ == '__main__':
    print(faker.past_datetime())
