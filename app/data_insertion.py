import json
import os.path
from pathlib import Path

from werkzeug.security import generate_password_hash

#
from Flask_Project.app.db_models import User

app_dir = Path(__file__).parent
json_path = os.path.join(app_dir, 'seeds/data_db.json')


class FillBase:
    def __init__(self, db, u_data):
        self.db = db
        self.u_data = u_data

    def append(self):
        process = self.db(
            first_name=self.u_data['first_name'],
            last_name=self.u_data['last_name'],
            age=self.u_data['age'],
            nickname=self.u_data['nickname'],
            password=self.u_data['password'],
            email=self.u_data['email'],
            is_admin=self.u_data['is_admin'],
            description=self.u_data['description'],
        )


if __name__ == '__main__':

    admin = {
        'age': 100,
        'nickname': 'admin',
        'password': generate_password_hash('admin'),
        'email': 'admin@gmail.com',
        'is_admin': True,
    }
    create_user = FillBase(User, admin)
    create_user.append()


    def load_json_data():
        with open(json_path, encoding='utf-8') as j_file:
            return json.load(j_file)


    for user_data in load_json_data():
        create_user = FillBase(User, user_data)
        create_user.append()
