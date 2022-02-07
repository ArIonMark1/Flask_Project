import os
from pathlib import Path

from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

"""
.. 
dialect:: postgresql+psycopg2
    :name: psycopg2
    :dbapi: psycopg2
    :connectstring: postgresql+psycopg2://user:password@host:port/dbname[?key=value&key=value...]
    :url: https://pypi.org/project/psycopg2/
"""

load_dotenv()
env_path = Path(__file__).parents[1] / '.env'  # путь к файлу .env
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('URI')
db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = LoginManager(app)

from Flask_Project.app import db_models

db.create_all()
from Flask_Project.app import mappings

# db.create_all()
# db.drop_all()
