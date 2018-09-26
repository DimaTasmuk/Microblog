from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from mongoengine import connect

from config import Config
from credentials import MONGO_URI, MONGO_DATABASE_NAME

app = Flask(__name__)
app.config.from_object(Config)
db = connect(db=MONGO_DATABASE_NAME, host=MONGO_URI)
login = LoginManager(app)
login.login_view = 'login'
mail = Mail(app)

from app import routes, models, errors
