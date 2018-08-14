from flask import Flask
from mongoengine import connect

from config import Config
from credentials import MONGO_URI, MONGO_DATABASE_NAME

app = Flask(__name__)
app.config.from_object(Config)
db = connect(db=MONGO_DATABASE_NAME, host=MONGO_URI)

from app import routes
