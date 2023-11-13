import os
import pyodbc, struct
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from _credential import server, driver, username, password

load_dotenv()
environment = os.getenv("FLASK_ENV") 
client_id = os.getenv("MANAGED_CLIENT_ID")  # Azure App environment variable os.environ["MANAGED_CLIENT_ID"]
connection_string_dev = os.getenv("AZURE_SQL_CONNECTIONSTRING_DEV")
connection_string_azmi = os.getenv("AZURE_SQL_CONNECTIONSTRING_AZMI")
#print(f'***** MANAGED_CLIENT_ID: {client_id=}')

def get_connection_string():
    if environment.lower() == 'dev':
        return connection_string_dev
    elif environment.lower() == 'prod':
        return connection_string_azmi
    else:
        print("***** Error wrong environment name. Check your .env file, environment must be dev or prod")

def get_conn():
    if environment.lower() == 'dev':
        return get_dev_conn()
    elif environment.lower() == 'prod':
        return get_azmi_conn()
    else:
        print("***** Error wrong environment name. Check your .env file, environment must be dev or prod")

# Use dev username and password. Do not push username and password in source control
def get_dev_conn():
    connection_string = get_connection_string()
    print(f'***** Dev Connect {connection_string=} \n')

    connection_string = connection_string.format(drv = driver, svr = server, uid = username, pwd = password)
    conn = pyodbc.connect(connection_string)
    return conn

# Use Azure managed identity
def get_azmi_conn():
    connection_string = get_connection_string()
    print(f'***** Prod Connect {connection_string=} \n')
    credential = DefaultAzureCredential(managed_identity_client_id=client_id)
    token_bytes = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
    token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
    SQL_COPT_SS_ACCESS_TOKEN = 1256  # This connection option is defined by microsoft in msodbcsql.h
    
    connection_string = connection_string.format(drv = driver, svr = server)
    conn = pyodbc.connect(connection_string, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})
    return conn   
