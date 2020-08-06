import os

class Config:
    SECRET_KEY = '7d71b24150d3b247d636816eda608561' #os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'#os.environ.get('SQLALCHEMY_DATABASE_URI')
    # to set up database and set its location we use config cmd
    # 3 fwd slashes means relative path to the database file from current location
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')