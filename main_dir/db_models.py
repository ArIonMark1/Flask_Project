import datetime

from flask_login import UserMixin, login_manager

from web_site.main_dir import db, manager


# *********************************************

class Users(db.Model, UserMixin):
    __tablename__ = 'user'
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

    def __init__(self, first_name, last_name, age, nickname, password, email, is_admin, description=None):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.nickname = nickname
        self.password = password
        self.email = email
        self.description = description  # описание пользователя по дефолту пустое, но в процессе работы на сайте можно добавить или редактировать
        self.is_admin = is_admin
        self.last_login = datetime.datetime.now()

    def __repr__(self):
        return f'{self.id}: {self.nickname}'


@manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)
