# models.py
from main import db


class User(db.Model):
    USERID = db.Column(db.Integer, primary_key=True)
    USERNAME = db.Column(db.String(120))
    PASSWORD = db.Column(db.String(120))
    EMAIL =db.Column(db.String(120))
    FULL_NAME = db.Column(db.String(120))
    PHONE_NUMBER = db.Column(db.Integer)
    REGISTRATION_TIME=db.Column(db.TIMESTAMP)
    LAST_LOGIN_TIME=db.Column(db.TIMESTAMP)
    USER_STATUS = db.Column(db.String(120))
    USER_TYPE = db.Column(db.String(120))
    COUNTRY = db.Column(db.String(120))
    CITY = db.Column(db.String(120))
