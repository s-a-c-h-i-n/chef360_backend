from flask import jsonify, request
from flask_jwt_extended import create_access_token
from repositories.userRepo import UserRepo
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from datetime import datetime, timezone, timedelta

userRepo = UserRepo()

def login():
        
        email = request.json['email']
        password = request.json['user_password']

        user = userRepo.login(email, password)
        if user:
            access_token = create_access_token(identity=email)
            return jsonify(message="Login succeeded!", access_token=access_token)
        else:
            return jsonify(message="Bad email or password"), 401
