from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
# the view that we pass in here is the function name of our route
# flashes default message "Please log in to access this page."
# customize the message by setting LoginManager.login_message
login_manager.login_message_category = 'info'   # info class is a blue information alert from Bootstrap

mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app

'''
In venv, python3 run.py
run.py -- from flaskblog (package) import app
Whenever flaskblog is interacted with, Flask will automatically search for an __init__ file within the package
In __init__.py, from flask import Flask, from flask_sqlalchemy import SQLAlchemy, app and db are instantiated
routes imported after app substantiated to avoid circular import; routes.py makes extensive use of app
Then returns to run.py to check if __name__ = '__main__' which is true, allowing package to run
'''

# past note: our routes.py file is importing this app variable; to avoid circular imports, we will import routes below (line 10)
# 3 /s specify a relative path; site.db file should get created in our project directory