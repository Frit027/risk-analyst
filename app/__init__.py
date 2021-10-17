from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/trial_1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'a78b1fe0e6491de8e9cf2a49a6e20c8f'

db = SQLAlchemy(app)

from app import models
# db.create_all()
from app import views
