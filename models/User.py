from dataclasses import dataclass
from sqlalchemy import Column, Integer, String, DateTime
from dbInstance import db

@dataclass
class User(db.Model):
    """User Model"""
    __tablename__ = 'user_profile'

    userid:int = Column(Integer, primary_key=True, autoincrement=True)
    e_mail:str = Column(String(50), unique=True)
    user_password:str = Column(String(255))
    full_name:str = Column(String(255))
    last_name:str = Column(String(255))
    phone_number:str = Column(String(10))
    registration_time:DateTime = Column(DateTime)
    last_login_time:DateTime = Column(DateTime)
    user_status:str = Column(String(10))
    user_type:str = Column(String(10))
    country:str = Column(String(10))
    city:str = Column(String(10))

