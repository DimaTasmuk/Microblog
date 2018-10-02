from flask import Flask, request
from flask_babel import Babel, _
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from mongoengine import connect

from config import Config
from credentials import MONGO_URI, MONGO_DATABASE_NAME

app = Flask(__name__)
app.config.from_object(Config)
db = connect(db=MONGO_DATABASE_NAME, host=MONGO_URI)
login = LoginManager(app)
login.login_view = 'login'
login.login_message = _('Please log in to access this page.')
mail = Mail(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
babel = Babel(app)


@babel.localeselector
def get_locale():
    # return request.accept_languages.best_match(app.config['LANGUAGES'])
    return 'ru'


from app import routes, models, errors
