from models.User import User
from dbInstance import db
from models.Blocklist import TokenBlocklist

class UserRepo:

    def __init__(self) -> None:
        pass

    def login(self, email, password):
        user = User.query.filter_by(e_mail=email, user_password=password).first()
        return user