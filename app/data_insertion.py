import json
import os.path
from pathlib import Path

app_dir = Path(__file__).parent
json_path = os.path.join(app_dir, 'seeds/data_db.json')


class FillBase:
    """ Класс заполнения таблицы пользователей """

    def __init__(self, database, u_data, session):
        self.database = database
        self.u_data = u_data
        self.session = session

    def create_user(self):
        process = self.database(
            first_name=self.u_data['first_name'],
            last_name=self.u_data['last_name'],
            age=self.u_data['age'],
            nickname=self.u_data['nickname'],
            password=self.u_data['password'],
            email=self.u_data['email'],
            is_admin=self.u_data['is_admin'],
            description=self.u_data['description'],
            last_login=self.u_data['last_login'],
        )
        self.session.add(process)
        self.session.commit()
