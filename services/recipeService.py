from flask import jsonify, request

def recipePromptGeneration():
    
    ingredients = request['ingredients']
    meal = request['meal']
    cookware = request['cookware']
    time = request['time']

    token = request.headers["Authorization"].split(" ")[1]
    if not token:
        return {
            "message" : "Authentication Token is missing!",
            "data" : None,
            "error" : "Unauthorized" 
        }, 401

    prompt = "Suggest"