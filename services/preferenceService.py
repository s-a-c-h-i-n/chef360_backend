from flask import jsonify, request
from flask_jwt_extended import create_access_token
from repositories.userPreferenceRepo import UserPreferenceRepo
from flask_jwt_extended import create_access_token, jwt_required, get_jwt,get_jwt_identity,decode_token
from datetime import datetime, timezone, timedelta
from JWTInstance import jwt
from repositories.stringOperator import splitUnderscores,mergeUnderscores
from tools.returnPattern import errorReturn
userPreferenceRepo = UserPreferenceRepo()

def getPreference():
    access_token = request.headers["Authorization"].split(" ")[1]
    decoded_token =decode_token(access_token)
    state, userPreference=userPreferenceRepo.getPreference(decoded_token["sub"])
    if state:
        cookware=splitUnderscores(userPreference.COOKWARE)
        allergics=splitUnderscores(userPreference.ALLERGICS)
        ret={
            "code":200,
            "message":"Success",
            "data":{
                    "EMAIL":userPreference.E_MAIL,
                    "COOKWARE":cookware,
                    "ALLERGICS":allergics
                }
        }
        return ret
    else:
        msg = errorReturn(404,"Not Found 404 error")
        return jsonify(message=msg), 404
    
def addPreference():
    data=request.get_json()
    access_token = request.headers["Authorization"].split(" ")[1]

    decoded_token =decode_token(access_token)
    state,userPreference=userPreferenceRepo.getPreference(decoded_token["sub"])
    
    if "cookware" in data:
        cookware = mergeUnderscores(data["cookware"])
    else:
        cookware= ''
    if "allergics" in data:
        allergics = mergeUnderscores(data["allergics"])
    else:
        allergics = ''
        
    if state:
        userPreferenceRepo.updatePreference(decoded_token["sub"],cookware,allergics)
    else:
        userPreferenceRepo.addPreference(decoded_token["sub"],cookware,allergics)
    return{
        "code":200,
        "message":"Success"
    }
