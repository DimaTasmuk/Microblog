# -*- coding: UTF-8 -*-
from app import login
from flask_login import UserMixin
from mongoengine import StringField, Document, ReferenceField, NULLIFY, DateTimeField
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, Document):
    username = StringField(required=True, unique=True)
    email = StringField(required=True, unique=True)
    password_hash = StringField(required=True)

    def __repr__(self):
        return '<User {} ({})>'.format(self.username, self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Post(Document):
    text = StringField(required=True)
    author = ReferenceField(User, reverse_delete_rule=NULLIFY)
    date = DateTimeField()

    def __repr__(self):
        return '<Post (author: {}, text: {}, date: {})>'.format(self.author, self.text, self.date)


@login.user_loader
def load_user(id):
    return User.objects.get(id=id)
