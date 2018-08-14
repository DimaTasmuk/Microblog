# -*- coding: UTF-8 -*-
from mongoengine import StringField, Document, ReferenceField, NULLIFY, DateTimeField


class User(Document):
    username = StringField(required=True)
    email = StringField(required=True, unique=True)
    password_hash = StringField(required=True)

    def __repr__(self):
        return '<User {} ({})>'.format(self.username, self.email)


class Post(Document):
    text = StringField(required=True)
    author = ReferenceField(User, reverse_delete_rule=NULLIFY)
    date = DateTimeField()

    def __repr__(self):
        return '<Post (author: {}, text: {}, date: {})>'.format(self.author, self.text, self.date)
