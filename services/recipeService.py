from flask import jsonify, request
from flask_jwt_extended import decode_token
import app as app
from models.User import User
from repositories.userPreferenceRepo import UserPreferenceRepo
from repositories.stringOperator import splitUnderscores
from repositories.userRepo import UserRepo
from repositories.recipeRepo import RecipeRepo
from _connection import get_conn
import json
userRepo=UserRepo()
userPreferenceRepo = UserPreferenceRepo()
recipeRepo=RecipeRepo()
def recipePromptGeneration(data):
    
    ingredients = data['ingredients']
    meal = data['meal']
    cookware = data['cookware']
    time = data['time']

    token = request.headers["Authorization"].split(" ")[1]
    if not token:
        return {
            "message" : "Authentication Token is missing!",
            "data" : None,
            "error" : "Unauthorized" 
        }, 401
    
    try:
        #data = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
        decoded_token =decode_token(token)
        e_mail = decoded_token["sub"]
        #current_user = User.query.filter_by(e_mail=decoded_token["sub"]).first()
        conn = get_conn()
        cursor = conn.cursor()
        row=cursor.execute("SELECT USERID,USER_PASSWORD,FULL_NAME,LAST_NAME,E_MAIL,PHONE_NUMBER,REGISTRATION_TIME,LAST_LOGIN_TIME,USER_STATUS,USER_TYPE,COUNTRY,CITY FROM dbo.USER_PROFILE WHERE E_MAIL=?",e_mail).fetchone()
        
        if row is None:
                return {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
            }, 401
    
    except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500

    user_preference = userPreferenceRepo.getPreference(decoded_token["sub"])
    allergics=splitUnderscores(user_preference.ALLERGICS)
    prompt = """Suggest one recipe for {0} with ingredients including {1} considering that I'm allergic to {2}. 
                I have these cookware - {3} and want it to be done in about {4} to {5} minutes. Provide the results only in Json format."""

    a=prompt.format(meal, ', '.join(ingredients), ',  '.join(allergics), ', '.join(cookware), time[0], time[1])
    return a
def storeRecipe():
    data=request.get_json()
    recipe = data['recipe']
    recipe_str=json.dumps(recipe)
    print(recipe_str)
    token = request.headers["Authorization"].split(" ")[1]
    if not token:
        return {
            "message" : "Authentication Token is missing!",
            "data" : None,
            "error" : "Unauthorized" 
        }, 401
    
    try:
        decoded_token =decode_token(token)
        e_mail = decoded_token["sub"]
        recipeRepo.addRecipe(e_mail,recipe_str)
        return{
            "code":200,
            "message":"Store recipe success"
        }
    except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500
    