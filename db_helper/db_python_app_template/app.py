import os
import pyodbc
import datetime
from _credential import server, driver, username, password
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for, jsonify
#from typing import Union
from pydantic import BaseModel
from flask_pydantic import validate

# Create an instance for the web App
app = Flask(__name__)

load_dotenv()
connection_string = os.getenv("AZURE_SQL_CONNECTIONSTRING")
response = ''

class Customer(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email_address: str | None = None #Union[str, None] = None
    priority: int
    
def get_conn():
    print(f'{driver=} \n')
    dev_connection_string = connection_string.format(drv = driver, svr = server, uid = username, pwd = password)
    #print(f'{dev_connection_string=}\n')
    conn = pyodbc.connect(dev_connection_string)
    return conn
    
    
@app.route("/api/create_table_customer", methods=["GET"])
def create_table_customer():
    print("Start create_table_customer")
    try:
        conn = get_conn()
        cursor = conn.cursor()

        # Table should be created ahead of time in production app.
        cursor.execute('''CREATE TABLE dbo.Customer (
                CustomerID INT IDENTITY(1,1) NOT NULL,
                FirstName VARCHAR(25) NOT NULL,
                LastName VARCHAR(25) NOT NULL,
                PhoneNumber VARCHAR(15) NOT NULL,
                EmailAddress VARCHAR(25) NULL,
                Priority INT NOT NULL,
                CreateDate DATETIME NOT NULL)ON [PRIMARY];
                
                ALTER TABLE [dbo].[Customer] ADD CONSTRAINT [DF_Customer_CreateDate] 
                DEFAULT (getdate()) FOR [CreateDate];
            ''')
            
        conn.commit()      
        conn.close(); 
        return "Success: Customer table created", 200
    except Exception as e:
        # Table may already exist
        print(f'Error {e}\n')
        return f"Error: {e}", 400


@app.route("/api/create_customer/", methods=["POST"])
def create_customer(item: Customer):
    print("Start create_customer")
    if item is null or not isinstance(item, Customer):
        raise TypeError("Item can not be null and must be of type customer")
        
    try:
        with get_conn() as conn:
            cursor = conn.cursor()
            sql = "INSERT INTO Customer (FirstName, LastName, PhoneNumber, EmailAddress, Priority, CreateDate) VALUES (?, ?, ?, ?, ?, ?)"
            cursor.execute(sql, item.first_name, item.last_name, item.phone, item.email_address, item.priority, datetime.datetime.now())
            conn.commit()

        return "Success: Customer record created", 200
    except Exception as e:
        # failed
        print(f'Error {e}\n')
        return f"Error: {e}", 400
       
@app.route("/api/get_all_customers", methods=["GET"])
def get_all_customers():
    rows = []

    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT TOP (10) * FROM dbo.Customer")
        #response = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        response = [dict(zip(columns, row)) for row in cursor.fetchall()]
       
        #print('\n')
        #for row in response:
            #print(row.FirstName, row.LastName)
            #print(row)
            #rows.append(f"{row.CustomerID}, {row.FirstName}, {row.LastName}")  
        # Fetch response
    
    if response is None or response == '':
        response = f"Response not found."
        return response, 400
        
    return jsonify(response), 200
    
    
if __name__ == '__main__':
    app.run()