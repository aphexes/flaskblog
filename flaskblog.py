from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'e8883e90b0d88a02978811153ba747a6'

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

@app.route("/register", methods=['GET', 'POST']) # list specifying methods allowed
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Register', form=form)

@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)

# this conditional is only true if we run the script with python directly;
# if we import the module to somewhere else, the name will be the name of the module
if __name__ == '__main__':
    app.run(debug=True)