import datetime

from flask_login import UserMixin
from Flask_Project.app.app import db, manager


# *********************************************

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    age = db.Column(db.Integer())
    nickname = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(100), default=None)
    is_admin = db.Column(db.Boolean(), default=False)
    last_login = db.Column(db.DateTime())

    def __repr__(self):
        return f'{self.__class__.__name__} : {self.nickname}'

    def __init__(self, nickname, email, password, is_admin, first_name=None, last_name=None, age=None,
                 description=None, last_login=None):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.nickname = nickname
        self.password = password
        self.email = email
        self.description = description  # описание пользователя по дефолту пустое, но в процессе работы на сайте можно добавить или редактировать
        self.is_admin = is_admin
        self.last_login = last_login


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
