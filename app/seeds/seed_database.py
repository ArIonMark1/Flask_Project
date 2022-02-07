import json

from werkzeug.security import generate_password_hash


from faker import Faker

faker = Faker('ru-RU')

print(faker.user_name())

with open('data_db.json', 'w', encoding='utf-8') as file:
    json_list = []
    for i in range(15):
        users_info = {
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "age": faker.random_int(20, 90),
            "nickname": faker.user_name(),
            "password": generate_password_hash(faker.password()),
            "email": faker.email(),
            "description": faker.text(),
            "is_admin": False, }
        json_list.append(users_info)

    file.write(json.dumps(json_list, sort_keys=True, ensure_ascii=False))
