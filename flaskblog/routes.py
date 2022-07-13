import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User, Post   # we place this here so that db is already defined when we run through model
from flask_login import login_user, current_user, logout_user, login_required
'''
posts = [
    {
        'author': 'Derek Chen',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'June 23, 2022'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'June 24, 2022'
    }
]'''

@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    # this grabs the posts and displays them on the home screen
    return render_template('home.html', comments=posts)
    # we are passing these posts into our home template and gaining access
    # to that variable in our home template as equal to our post data

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST']) # list specifying allowed methods
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # .decode('utf-8') makes it a string instead of bytes
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)    # these two lines add a user to the database
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        # bootstrap has different alert styles for success, warning, and danger
        return redirect(url_for('login'))
        # again, home refers to the FUNCTION name in line 25 and not the url path
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])   # POST is more secure; cannot be seen, even without being encrypted
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
            return redirect(next_page) if next_page else redirect(url_for('home'))
            # this is called a ternary conditional; if next_page is None/False then we just redirect home
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")   # don't need to specify default 'GET' method
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    # we are splitting the ext (file type) from the file name (f_name)
    # we can store the filename in the _ variable that we will NOT use
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    # app.root.path gives us the full path up to the package directory

    output_size = (125, 125)    # tuple specifying dimension in px
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
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
        return redirect(url_for('account'))
        # you want to use redirect instead of letting it fall down to the render template line
        # because of the POST/GET redirect pattern
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    # image_file defined in the User model, line 14 of models.py
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    # this gives us the posts with the post_id or returns a 404 error page
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)  # http response for a forbidden route
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))