from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from market.config import SQLALCHEMY_DATABASE_URI, SECRET_KEY


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = SECRET_KEY
db = SQLAlchemy(app)

from market import routes

