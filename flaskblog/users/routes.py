from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post   # we place this here so that db is already defined when we run through model
from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from flaskblog.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)

# we're creating routes specifically for the users blueprint
@users.route("/register", methods=['GET', 'POST']) # list specifying allowed methods
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # .decode('utf-8') makes it a string instead of bytes
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)    # these two lines add a user to the database
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        # bootstrap has different alert styles for success, warning, and danger
        return redirect(url_for('users.login'))
        # again, home refers to the FUNCTION name in line 25 and not the url path
    return render_template('register.html', title='Register', form=form)

@users.route("/login", methods=['GET', 'POST'])   # POST is more secure; cannot be seen, even without being encrypted
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        # if form.email.data == 'admin@blog.com' and form.password.data == 'password':
        # flash('You have been logged in!', 'success')
        # return redirect(url_for('home'))
    # else:
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
        # compares user.password (from the database) to form.password.data (user input password)
            login_user(user, remember=form.remember.data)   # remember is a True/False value (checkbox)
            next_page = request.args.get('next')    # args is a dictionary; using the get method will return None if the next parameter doesn't exist
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
            # this is called a ternary conditional; if next_page is None/False then we just redirect home
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")   # don't need to specify default 'GET' method
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
        # you want to use redirect instead of letting it fall down to the render template line
        # because of the POST/GET redirect pattern
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    # image_file defined in the User model, line 14 of models.py
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    # get the first user with this username or return 404; similar to GET method but doesn't search by id
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token.', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)