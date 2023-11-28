from flask import jsonify, request
from flask_jwt_extended import create_access_token
from repositories.userRepo import UserRepo
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from datetime import datetime, timezone, timedelta
import time
import re
import jwtTool

userRepo = UserRepo()

def login():
        
        email = request.json['email']
        password = request.json['user_password']

        user = userRepo.login(email, password)
        if user:
            access_token = create_access_token(identity=email, expires_delta=False)
            return jsonify(message="Login succeeded!", access_token=access_token)
        else:
            return jsonify(message="Bad email or password"), 401

def register():
    validate_phone_number_pattern = "^\\+?[1-9][0-9]{7,14}$"
    data = request.get_json()
    USER_PASSWORD = data['USER_PASSWORD']
    FULL_NAME = data['FULL_NAME']
    LAST_NAME = data['LAST_NAME']
    E_MAIL = data['E_MAIL']
    PHONE_NUMBER = data['PHONE_NUMBER']

    match = re.match(validate_phone_number_pattern, PHONE_NUMBER)
    if match is None:
        return jsonify(message="Incorrect Phone Number"), 401

    COUNTRY = data['COUNTRY']
    CITY = data['CITY']
    USER_STATUS = 'ONLINE'
    USER_TYPE = 'REGULAR_USER'
    REGISTRATION_TIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    LAST_LOGIN_TIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    result=userRepo.checkRegister(E_MAIL)
    if result!='Good':
        return jsonify(message=result), 400

    E_MAIL=userRepo.register(USER_PASSWORD, FULL_NAME, LAST_NAME, E_MAIL, PHONE_NUMBER, REGISTRATION_TIME,
                LAST_LOGIN_TIME, USER_STATUS, USER_TYPE, COUNTRY, CITY)

    if E_MAIL:
        access_token = create_access_token(identity=E_MAIL)
        return jsonify(message="Register succeeded!", access_token=access_token)
    else:
        return jsonify(message="Bad email or password"), 401

def errorReturn(code,message):
    ret={
            "code":code,
            "message":message
        }
    return ret

def getPersonalInfor():
    access_token=request.headers["Authorization"].split(" ")[1]
    data,expired,state,message=jwtTool.decodeToken(access_token)
    if(state==False):
        if(str(message)=="Signature has expired"):
            return errorReturn(401,str(message))
        return errorReturn(300,str(message))
    if expired==True:
        return errorReturn(401,"This user already expired")

    result=userRepo.getPersonalInfor(data['sub'])
    if result['code']==200:
        return result
    else:
        return errorReturn(404,"Not found")
