# Azure environment:
	(Help) https://medium.com/@pratikkrsharma/deploy-python-flask-api-on-azure-easy-and-fast-way-e5839bd09e47
	(Help) https://towardsdatascience.com/deploy-fastapi-on-azure-with-github-actions-32c5ab248ce3
## Resource Group: app-chef360-v1-rg
## App Service Name: app-cheef360-ai-helper

# Production deployment
	In Production you need a WSGI: https://flask.palletsprojects.com/en/3.0.x/deploying/
		For instance add Gunicorn to requirement packages to install.
	Deployment to Prod tutorial: https://flask.palletsprojects.com/en/3.0.x/tutorial/deploy/

# Development environment
	In powershell:
	- Navigate into the project directory
		cd FlaskEndpoint
	- Make a copy of the example environment variables file '.env.example' into '.pp-env'. (if you use environment variables)
		cp .env.example .env
			or
		copy .env.example .env
		
	- Create environment, Install the dependencies and run the example app:
		you may need to type python3/pip3 instead of python/pip depending on your setup.	
			Create environment: 		python -m venv venv
			Activate environment: 		. venv/Scripts/activate
									or 
										source venv/Scripts/activate
			Install requirements: 		pip install -r requirements.txt	

			run App with Flask:			flask run
			or run in debug mode:		flask --app app run --debug --no-debugger --no-reload
										flask --app app.py --debug run


# You must complete the following values in your .env environment file. Make sure to not share it with anyone! The API information must remain private.
OPENAI_API_KEY="********************"
# Azure key vault names used for request authentications (user -> ai-helper-api | ai-helper-api -> chatgpt-api)
API_USER_KEY_VAULT_NAME="user_key_vault"
SECRET_NAME="user_secret_password"

# Api Log files - Only Admin has access to see logs:
(App Service Log) https://app-cheef360-ai-helper.scm.azurewebsites.net/api/vfs/LogFiles/
(Log Stream) https://portal.azure.com/#@uottawa.onmicrosoft.com/resource/subscriptions/2571a70a-c023-4cfe-b82e-4f03584d6297/resourceGroups/app-chef360-v1-rg/providers/Microsoft.Web/sites/app-cheef360-ai-helper/logStream

# Azure key vault
https://medium.com/analytics-vidhya/keep-your-secrets-safe-with-azure-key-vault-in-python-9848be3230db