# from werkzeug.security import generate_password_hash
# import random
# from web_site.app.db_models import User
# import os
# from pathlib import Path
# from dotenv import load_dotenv
#
# from flask_seeder import FlaskSeeder, Seeder, Faker, generator
# from web_site.app.app import db, app  # Or wherever you would get your session
# import json

# load_dotenv()
# env_path = Path(__file__).parents[1] / '.env'
# load_dotenv(dotenv_path=env_path)
# #
# db.init_app(app)


# class DemoSeeder(Seeder):
#
#     def run(self):
#         faker = Faker(
#             cls=User,
#
#             init={
#                 "id": generator.Sequence(),
#                 "first_name": generator.String(),
#                 "last_name": generator.String(),
#                 "age": generator.Integer(start=20, end=90),
#                 "nickname": generator.String(),
#                 "password": generator.Integer(),
#                 "email": generator.Email(),
#                 "description": generator.String(),
#                 "is_admin": generator.String(),
#             }
#         )
#
#         # Create 5 users
#         for user in faker.create(1):
#             print(f"Adding user: {user}")
#             print(f'{faker}')
#             self.db.session.add(user)
#
#         with open('data_db.json', 'w', encoding='utf-8') as file:
#             for user in faker.create("12"):
#                 file.write(json.dumps(user))



import factory
from myapp.models import Book

class BookFactory(factory.Factory):
    class Meta:
        model = Book

    title = factory.Faker('sentence', nb_words=4)
    author_name = factory.Faker('name')






