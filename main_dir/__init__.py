from flask import Flask, render_template, url_for, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.secret_key = 'resurrection'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:1401@127.0.0.1:8000/work_project"
db = SQLAlchemy(app)
manager = LoginManager(app)

from web_site.main_dir import db_models, mappings
db.create_all()
# db.drop_all()

