import os

from credentials import GMAIL_USERNAME, GMAIL_PASSWORD, ADMIN_EMAIL


class Config(object):
    SECRET_KEY = "mDAR8eK9buA62NXqLsMtaDvHLLeHapGms4hgh34h5rcwQ99fH9RLL"

    POSTS_PER_PAGE = 25

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = "587"
    MAIL_USE_TLS = 1
    MAIL_USERNAME = GMAIL_USERNAME
    MAIL_PASSWORD = GMAIL_PASSWORD
    ADMIN = ADMIN_EMAIL

    LANGUAGES = ['ru', 'en', 'ua']

    APP_PATH = os.path.dirname(os.path.abspath(__file__))
