# chef360_backend

* We will add code to the main branch and will eventually use this branch to deploy our app.

## Development environment
	In powershell:
	- Navigate into the project directory
		cd 
	- Connect to Azure sql to confirm that you can see the dev db (use your @uottawa account in Azure)

	- Create python environment and activate it:
				py -m venv .venv
				.venv\scripts\activate
	- Install requirements:
				pip install -r requirements.txt 

	- Create your env file 
				cp .env.example .env
	- When you develop locally, open the .env file update these variables. For production, the key is set with a Azure environment variable.
 		* Rename this environment variable to 'dev':
				FLASK_ENV='dev'
    		* Add le openAI key:
      				OPENAI_APIKEY_RECIPE='*****my_openai_key*****'
				
	- Create a your credential file 
				cp _credential.template.py _credential.py
	- For local development, update your _credential.py file with your SQL servername, username and password to access the db. This is not your @uottawa account!!
		(DO NOT SHARE THE CREDENTIAL OR PUSH IT TO SOURCE CONTROL)
  
	- For production deployment, a user managed identity "Chef360..." was created and used in Azure App service.

	- The db connection string is already defined in .env file (do not change it)
	
	- Run:
		flask run			
	- To debug run:
		flask --app app.py --debug run
				


