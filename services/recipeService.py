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

    user_preference = userPreferenceRepo.getPreference(decoded_token["sub"])[1]
    if user_preference != None:
        allergics=splitUnderscores(user_preference[-1])
        print(f"test*{allergics=}*test\n")
    
    if allergics != None None and allergics != "":
        prompt = """Suggest one recipe for {0} with ingredients including {1} considering that I'm allergic to {2}. 
                I have these cookware - {3} and want it to be done in about {4} to {5} minutes. Provide the results only in Json format."""
    
        a=prompt.format(meal, ', '.join(ingredients), ',  '.join(allergics), ', '.join(cookware), time[0], time[1])
        print(f"*(1) prompt {a=}\n")
        return a
    else:
        prompt = """Suggest one recipe for {0} with ingredients including {1}. 
                 I have these cookware - {2} and want it to be done in about {3} to {4} minutes. Provide the results only in Json format."""
        a = prompt.format(meal, ', '.join(ingredients), ', '.join(cookware), time[0], time[1])
        print(f"*(2) prompt {a=}\n")
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
    
def getRecipe():
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
        state,recipes=recipeRepo.getRecipe(e_mail)
        if(state):

            print(recipes)
            print(7)
            data=[]
            for i in recipes:
                print(i)
                print(type(i))
                data.append(list(i))
                #print(json.dumps(i))
            print(data)
            print(8)
            jsonRecipes=pyodbc2Json(recipes)
            return{
                "code":200,
                "message":"success",
                "data":
                    jsonRecipes
                    
            }
        else:
            return{
                "code":200,
                "message":"No recipe",
                "data":""
            }
        
    except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500
    

def pyodbc2Json(data):
    print("in")
    jsonList=[]
    k=1
    for row in data:
        result={}
        result['recipe']=json.loads(row[0])
        result['index']=k
        k=k+1
        jsonList.append(result)
    print(jsonList)
    return jsonList
   
