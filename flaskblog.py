from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e8883e90b0d88a02978811153ba747a6'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# 3 /s specify a relative path; site.db file should get created in our project directory
db = SQLAlchemy(app)

class User(db.Model):
    id         = db.Column(db.Integer, primary_key=True)    # primary_key is a unique id for our user
    username   = db.Column(db.String(20), unique=True, nullable=False)   # 20 character max length, must be unique, can't null bc username required
    email      = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password   = db.Column(db.String(60), nullable=False)
    posts      = db.relationship('Post', backref='author', lazy=True)    # runs in the background b/c not a column
    # backref allows us to use the author attribute to get the user who created the post

    def __repr__(self):     # __repr__ is a special method used to represent a class’s objects as a string
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # current time req datetime module; no parentheses at end of datetime.utcnow in order to pass the function as an argument and not the current time
    # if we run it with parentheses, the time you set it will permanently be the time displayed
    content     = db.Column(db.Text, nullable=False)
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # user.id is going to be the user who authored the post

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

# post model and user model will have a relationship since users will author posts; this is a one-to-many relationship
# bc a users can have many posts but a post can only have one user; in the User class we are s


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
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', comments=posts)
    # we are passing these posts into our home template and gaining access
    # to that variable in our home template as equal to our post data

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST']) # list specifying allowed methods
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        # bootstrap has different alert styles for success, warning, and danger
        return redirect(url_for('home'))
        # again, home refers to the FUNCTION name in line 25 and not the url path
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check username and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

# this conditional is only true if we run the script with python directly;
# if we import the module to somewhere else, the name will be the name of the module
if __name__ == '__main__':
    app.run(debug=True)