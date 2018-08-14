from datetime import datetime
from uuid import uuid4

from flask import render_template, redirect, flash, url_for
from werkzeug.security import generate_password_hash

from app import app, db
from app.forms import LoginForm
from app.models import User, Post


@app.route("/")
@app.route("/index")
def index():
    user = {"username": "Dima"}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        },
        {
            'author': {'username': 'Ипполит'},
            'body': 'Какая гадость эта ваша заливная рыба!!'
        }
    ]
    return render_template('index.html', title='Home Page', user=user, posts=posts)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route("/add", methods=['GET', 'POST'])
def add():
    user = User(
        username='Dima',
        email='dimatasmuk@gmail.com',
        password_hash=generate_password_hash('dima'))
    user.save()

    post = Post(date=datetime.now(), author=user, text="Hello")
    post.save()
