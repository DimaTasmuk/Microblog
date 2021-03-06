from datetime import datetime

from flask_login import current_user, login_user, logout_user, login_required
from flask_babel import _, get_locale

from flask import render_template, redirect, flash, url_for, request, abort, g
from werkzeug.urls import url_parse

from pagination import Pagination
from app import app
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm, ResetPasswordRequestForm, \
    ResetPasswordForm
from app.models import User, Post
from app.email import send_password_reset_email


@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
@login_required
def index():
    page = request.args.get("page", 1, type=int)

    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user.id, date=datetime.utcnow())
        post.save()
        return redirect(url_for('index'))

    posts = current_user.get_followed_posts(page)
    pagination = Pagination(posts, page)
    next_url = url_for('index', page=pagination.next_num()) if pagination.has_next() else None
    prev_url = url_for('index', page=pagination.prev_num()) if pagination.has_prev() else None
    return render_template('index.html', title='Home Page', form=form, posts=posts, next_url=next_url, prev_url=prev_url)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.objects(username__iexact=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(category='error', message=_('Invalid username or password'))
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.save()
        flash(_('Congratulations, you are now a registered user!'))
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    page = request.args.get("page", 1, type=int)

    user = User.objects(username__iexact=username).first()
    if user is None:
        abort(404)

    posts = Post.get_user_posts(user)
    pagination = Pagination(posts, page)
    posts = pagination.paginate()
    next_url = url_for('user', username=user.username, page=pagination.next_num()) if pagination.has_next() else None
    prev_url = url_for('user', username=user.username, page=pagination.prev_num()) if pagination.has_prev() else None
    return render_template("user.html", user=user, posts=posts, next_url=next_url, prev_url=prev_url)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        current_user.save()
        flash(_("Your changes have been saved."))
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template("edit_profile.html", title="Edit profile", form=form)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        current_user.save()
    g.locale = str(get_locale())


@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.objects(username__iexact=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('index'))
    if user == current_user:
        flash(_("You cannot follow yourself"))
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    flash(_('You are following %(username)s!', username=username))
    return redirect(url_for('user', username=username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.objects(username__iexact=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('index'))
    if user == current_user:
        flash(_("You cannot unfollow yourself"))
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    flash(_('You are not following %(username)s!', username=username))
    return redirect(url_for('user', username=username))


@app.route('/explore')
@login_required
def explore():
    page = request.args.get("page", 1, type=int)

    posts = Post.get_all_posts(page)
    pagination = Pagination(posts, page)
    next_url = url_for('explore', page=pagination.next_num()) if pagination.has_next() else None
    prev_url = url_for('explore', page=pagination.prev_num()) if pagination.has_prev() else None
    return render_template('index.html', title='Explore', posts=posts, next_url=next_url, prev_url=prev_url)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.objects(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(_('Check your email for the instructions to reset your password'))
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        user.save()
        flash(_('Your password has been reset'))
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)
