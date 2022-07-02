import bcrypt
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)   # our routes.py file is importing this app variable; to avoid circular imports, we will import routes below (line 10) 
app.config['SECRET_KEY'] = 'e8883e90b0d88a02978811153ba747a6'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# 3 /s specify a relative path; site.db file should get created in our project directory
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
# the view that we pass in here is the function name of our route
# flashes default message "Please log in to access this page."
# customize the message by setting LoginManager.login_message
login_manager.login_message_category = 'info'   # info class is a blue informatiion alert from Bootstrap
from flaskblog import routes

'''
In venv, python3 run.py
run.py -- from flaskblog (package) import app
Whenever flaskblog is interacted with, Flask will automatically search for an __init__ file within the package
In __init__.py, from flask import Flask, from flask_sqlalchemy import SQLAlchemy, app and db are instantiated
routes imported after app substantiated to avoid circular import; routes.py makes extensive use of app
Then returns to run.py to check if __name__ = '__main__' which is true, allowing package to run
'''