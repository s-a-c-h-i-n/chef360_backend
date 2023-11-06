import openai
import os
from dotenv import load_dotenv
from toolbox import HelperTools
from flask import Flask, redirect, render_template, request, url_for, jsonify

# Create an instance for the web App
app = Flask(__name__)
app.config['DEBUG'] = False
app.config['TESTING'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

load_dotenv()
openai.api_key = os.getenv['OPENAI_API_KEY']  # This line causes some issues in azure. You can add the key here temporarly or as an azure variable 
temperature = 0.6
max_tokens = 4000

request_keys = ['ingredients', 'allergies']

prompt_request = """Suggest {0} {1} with ingredients including {2}; 
                 considering that I'm allergic to {3}. Provide the results only in Json format."""

result = {
    'response': '',
    'json_response': None,
    'http_code': 400
    }

tools = HelperTools()
file_path = "static"
file_name = "temp_source.json"

@app.route("/api/ping", methods=["GET"])
def ping():
    message = "ping recipe...\n"
    http_response_code = 200
    
    response = {'message': message, 'response': { 'type': 'Test API', 'msg': 'PONG NOODLES' }}
    return jsonify(response), http_response_code   
 
'''
Real function to use for recipe generation
'''
@app.route('/api/get_recipe/<int:nbrOfResults>/', methods=("POST", "GET"))
def get_recipe(nbrOfResults):
    # We will use a json format to send the transaction with all keys: ingredients and allergies.
    json_data_request = request.get_json()
    print(f"json_data_request={json_data_request}\n")
    
    # Iterate to verify if all required keys are in the json_data_request received.
    if not all (key in json_data_request for key in request_keys): # if not, bad request
        return 'Bad request: Missing transaction keys! You must specify ingredients and allergies in your json request', 400
    
    # # *****Get api_key with key from request. Should not be passed as url parameter.
    # api_key_user = request.headers.get("api-key")
    # print(f"api_key_user=...{api_key_user[-5:]}\n")
    
    # # Get key vault secret for authentication and verify credential.
    # tools.get_secret("API_USER_KEY_VAULT_NAME", "SECRET_NAME")
    # is_valid = tools.is_valid_user_request(api_key_user)
    # if not is_valid:
        # return 'Unauthorized request: Authentication failed! Confirm that you use the right auth key.', 401
    
    # Format user specification request entries
    user_specs = tools.stringify_request(json_data_request, request_keys)
    
    # Format prompt request to send to chatgpt
    user_request = tools.generate_ai_prompt_msg(prompt_request, nbrOfResults, user_specs)
  
    print(f"openai.api_key=...{openai.api_key[-5:]}\n")
    
    response = openai.Completion.create(
            model = "gpt-3.5-turbo-instruct",
            prompt = user_request,
            temperature = temperature,
            max_tokens = max_tokens)

    # Make sure to return a json
    result['response'] = response.choices[0].text
    if result['response'] is None or result['response'] == '':
        result['json_response'] = f"Adequat response not found."
    else:
        result['json_response'] = jsonify(result['response'])
        result['http_code'] = 200
    
    print(f"Openai help requested. Expected response...\n")
    return result['json_response'], result['http_code']

'''
 Temp fake function to return fake json for testing.
'''
@app.route("/api/get_fake_recipe/<int:nbrOfResults>/", methods=("POST", "GET"))
def get_recipes(nbrOfResults):
    message = "Error -> Failed to generate recipes!!"
    http_response_code = 500
    result = ""
    
    try:
        # Get request
        #json_data_request = request.get_json()
        
        # Check security with request header
  
        # Read temp file
        imported_data = tools.read_json_file(f"{file_path}/{file_name}")
        
        # Verify and return file
        if bool(imported_data):
            message = "Recipes generated successfully!!"
            http_response_code = 200
        else:
            message = f"Error -> Cannot find or access {file_name}"
            http_response_code = 404
                       
        response = {'message': message, 'response': imported_data}
        return jsonify(response), http_response_code
    
    except Exception as err:
            print(f"Error -> get_recipes: {err}")
            return jsonify({'message': message + err, 'new_block': result}), http_response_code



'''
# Runnig app to make it publicly available in your network.
# Or use host = 127.0.0.1 to be only accessible the computer running the app.
# Post number from 5000 can be changed to have multiple nodes. 
# To set a new node, Clone this file and change the port to 5001 for example.
'''
if __name__ == '__main__':
    # Running prod
    app.run()
    # app.run(debug=True, use_debugger=False, use_reloader=False)
