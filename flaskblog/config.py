import os

class Config:
    # we remove app.config[''] to make these constant variables
    # these can be automatically forwarded to a specified admin upon errors
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    # implements the relational query language SQL, useful for apps that have structured data
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True     # boolean flag to enable encrypted connections
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')