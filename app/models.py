# -*- coding: UTF-8 -*-
from datetime import datetime
from time import time

import jwt

from Utils import Pagination
from app import login, app
from flask_login import UserMixin
from mongoengine import StringField, Document, ReferenceField, NULLIFY, DateTimeField, ListField, Q
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5


class User(UserMixin, Document):
    username = StringField(required=True, unique=True)
    email = StringField(required=True, unique=True)
    password_hash = StringField(required=True)
    about_me = StringField(max_length=140)
    last_seen = DateTimeField(default=datetime.utcnow)
    followed = ListField(ReferenceField('self'))

    def __str__(self):
        return '<User {} ({})>'.format(self.username, [user.username for user in self.followed])

    def __repr__(self):
        return '<User {} ({})>'.format(self.username, [user.username for user in self.followed])

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
            self.followed.append(user)
            self.save()

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            self.save()

    def is_following(self, user):
        return user in self.followed

    def get_followers(self):
        return User.objects(followed=self)

    def get_followed_posts(self, page):
        posts = Post.objects(Q(author__in=self.followed) | Q(author=self)).order_by('-date')
        return Pagination(posts, page).paginate()

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.objects(id=id).first()


class Post(Document):
    body = StringField(required=True)
    author = ReferenceField(User, reverse_delete_rule=NULLIFY)
    date = DateTimeField()

    def __repr__(self):
        return '<Post (author: {}, body: {}, date: {})>'.format(self.author, self.body, self.date)

    def __str__(self):
        return '<Post (author: {}, body: {}, date: {})>'.format(self.author, self.body, self.date)

    @staticmethod
    def get_all_posts(page):
        posts = Post.objects().order_by('-date')
        return Pagination(posts, page).paginate()

    @staticmethod
    def get_user_posts(user):
        return Post.objects(author=user).order_by('-date')


@login.user_loader
def load_user(id):
    return User.objects.get(id=id)
