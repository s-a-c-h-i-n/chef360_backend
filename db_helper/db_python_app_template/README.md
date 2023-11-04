# Create a python Api using Azure sql db
	This is a template guide to help in Api creation to interact with our dev bd in Azure. You have been granted access to the bd with your @ottawa.
	Help: https://learn.microsoft.com/en-us/azure/azure-sql/database/azure-sql-python-quickstart?view=azuresql&tabs=windows%2Csql-auth

## Prerequisits:
	- Download Microsoft ODBC Driver 18 for SQL Server and install it in your computer: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16
	- pyodbc package and other python packages: installed with requirements.txt command
	- Azure db created with the credentials to access it (will use username password for dev)
	
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
	- Create a your env file 
				cp .env.example .env
	- Create a your credential file 
				cp _credential.template.py _credential.py
	- Update your local _credential.py file with your SQL servername, username and password to access the db. This is not your @uottawa account!!
		(DO NOT SHARE THE CREDENTIAL OR PUSH IT TO SOURCE CONTROL)		
	- The db connection string is already defined in .env file
	
	- Run:
		flask run			
	- To debug run:
		flask --app app.py --debug run
				


