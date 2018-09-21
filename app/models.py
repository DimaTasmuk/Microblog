# -*- coding: UTF-8 -*-
from datetime import datetime

from app import login
from flask_login import UserMixin
from mongoengine import StringField, Document, ReferenceField, NULLIFY, DateTimeField, ListField
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5


class User(UserMixin, Document):
    username = StringField(required=True, unique=True)
    email = StringField(required=True, unique=True)
    password_hash = StringField(required=True)
    about_me = StringField(max_length=140)
    last_seen = DateTimeField(default=datetime.utcnow)
    followers = ListField(ReferenceField('self'))
    following = ListField(ReferenceField('self'))

    def __repr__(self):
        return '<User {} ({})>'.format(self.username, self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.following.append(user)
            self.save()

    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)
            self.save()

    def is_following(self, user):
        return user in self.following

class Post(Document):
    text = StringField(required=True)
    author = ReferenceField(User, reverse_delete_rule=NULLIFY)
    date = DateTimeField()

    def __repr__(self):
        return '<Post (author: {}, text: {}, date: {})>'.format(self.author, self.text, self.date)


@login.user_loader
def load_user(id):
    return User.objects.get(id=id)
