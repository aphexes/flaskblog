from datetime import datetime
from itsdangerous import URLSafeTimedSerializer as Serializer
from flaskblog import db, login_manager, app    # we can import from flaskblog instead of __main__ now, using the __init__.py file
from flask_login import UserMixin

@login_manager.user_loader  # @ denotes a decorator
def load_user(user_id):
    return User.query.get(int(user_id))    # gets the user with that id and casts it to an integer
    #user_id naming convention required

class User(db.Model, UserMixin):
    id         = db.Column(db.Integer, primary_key=True)    # primary_key is a unique id for our user
    username   = db.Column(db.String(20), unique=True, nullable=False)   # 20 character max length, must be unique, can't null bc username required
    email      = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password   = db.Column(db.String(60), nullable=False)
    posts      = db.relationship('Post', backref='author', lazy=True)    # runs in the background b/c not a column
    # backref allows us to use the author attribute to get the user who created the post

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

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

# post model and user model will have a relationship since users will author posts;
# this is a one-to-many relationship bc a users can have many posts but a post can only have one user