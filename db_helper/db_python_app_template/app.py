import os
import pyodbc
import json
import datetime
from _credential import server, driver, username, password
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for, jsonify
#from typing import Union
import sys
sys.path.append('./tools')
import time

from pydantic import BaseModel
from flask_pydantic import validate
import tools.jwtTool as jwtTool
import tools.stringOperator as stringOperator
from tools.returnPattern import errorReturn

# Create an instance for the web App
app = Flask(__name__)

load_dotenv()
connection_string = os.getenv("AZURE_SQL_CONNECTIONSTRING")
response = ''

start=2

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

@app.route("/api/testToken",methods=["POST"])
def getTestToken():
    data={"name":"test",'USERID':1}
    token=jwtTool.generateToken(data)
    print("generated test token:",token)
    return token

@app.route("/api/getUserInformation",methods=['POST'])
def getUserInformation():
    argsJson = request.data.decode('utf-8')
    argsJson = json.loads(argsJson)
    token=argsJson['token']
    data,expired,state,message=jwtTool.decodeToken(token)
    if(state==False):
        if(str(message)=="Signature has expired"):
            return errorReturn(400,str(message))
        return errorReturn(300,str(message))
    if expired==True:
        return errorReturn(400,"This user already expired")
    with get_conn() as conn:
        cursor = conn.cursor()
        row=cursor.execute("SELECT USERID,USERNAME,USER_PASSWORD,FULL_NAME,LAST_NAME,E_MAIL,PHONE_NUMBER,REGISTRATION_TIME,LAST_LOGIN_TIME,USER_STATUS,USER_TYPE,COUNTRY,CITY FROM dbo.USER_PROFILE WHERE USERID=?",data['USERID']).fetchone()
        if(row is None):
            return errorReturn(404,"Not found")
        row.USERID = row.USERID
        row.USERNAME=stringOperator.splitUnderscores(row.USERNAME)
        row.FULL_NAME = stringOperator.splitUnderscores(row.FULL_NAME)
        row.LAST_NAME = stringOperator.splitUnderscores(row.LAST_NAME)
        row.E_MAIL = stringOperator.splitUnderscores(row.E_MAIL)
        row.PHONE_NUMBER = row.PHONE_NUMBER
        row.REGISTRATION_TIME = row.REGISTRATION_TIME
        row.LAST_LOGIN_TIME = row.LAST_LOGIN_TIME
        row.USER_STATUS = stringOperator.splitUnderscores(row.USER_STATUS)
        row.USER_TYPE = stringOperator.splitUnderscores(row.USER_TYPE)
        row.COUNTRY = stringOperator.splitUnderscores(row.COUNTRY)
        row.CITY = stringOperator.splitUnderscores(row.CITY)
        print(row)
        ret={
            "code":200,
            "message":"success",
            "data":{
                "USERID":row.USERID,
                "USERNAME":row.USERNAME,
                "FULL_NAME":row.FULL_NAME,
                "LAST_NAME": row.LAST_NAME,
                "E_MAIL": row.E_MAIL,
                "PHONE_NUMBER": row.PHONE_NUMBER,
                "REGISTRATION_TIME": row.REGISTRATION_TIME,
                "LAST_LOGIN_TIME": row.LAST_LOGIN_TIME,
                "USER_STATUS": row.USER_STATUS,
                "USER_TYPE": row.USER_TYPE,
                "COUNTRY": row.COUNTRY,
                "CITY": row.CITY,
            }
        }
        return ret
    return errorReturn(404,"Not found")

@app.route("/api/Register",methods=['POST'])
def Register():
    USERNAME=request.form['USERNAME']
    USER_PASSWORD = request.form['USER_PASSWORD']
    FULL_NAME = request.form['FULL_NAME']
    LAST_NAME = request.form['LAST_NAME']
    E_MAIL = request.form['E_MAIL']
    PHONE_NUMBER = request.form['PHONE_NUMBER']
    COUNTRY = request.form['COUNTRY']
    CITY = request.form['CITY']
    USER_STATUS = 'ONLINE'
    USER_TYPE = 'REGULAR_USER'
    REGISTRATION_TIME = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    LAST_LOGIN_TIME = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    global start
    with get_conn() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO dbo.USER_PROFILE VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",(start,USERNAME,USER_PASSWORD,FULL_NAME,LAST_NAME,E_MAIL,PHONE_NUMBER,REGISTRATION_TIME,LAST_LOGIN_TIME,USER_STATUS,USER_TYPE,COUNTRY,CITY))
        start+=1
        conn.commit()
    return USERNAME


    
if __name__ == '__main__':
    app.run(debug=True)
