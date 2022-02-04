from flask import Flask, render_template, url_for, request, flash, redirect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.secret_key = '7b1ffd40c08c86e3e4b47a4b392f6b04dccdbf3e'


app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:1401@127.0.0.1:8000/work_project"
db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = LoginManager(app)

from web_site.main_dir import db_models, mappings
db.create_all()
# db.drop_all()

