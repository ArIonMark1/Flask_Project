import os
from pathlib import Path

from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_seeder import FlaskSeeder

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

load_dotenv()
env_path = Path(__file__).parents[1] / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('URI')
db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = LoginManager(app)

seeder = FlaskSeeder()
seeder.init_app(app, db)

from web_site.app import db_models, mappings

db.create_all()
# db.drop_all()
