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


from pydantic import BaseModel
from flask_pydantic import validate
import jwtTool
import stringOperator
from returnPattern import errorReturn

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

@app.route("/api/testToken",methods=["POST"])
def getTestToken():
    data={"name":"test",'USERID':1}
    token=jwtTool.generateToken(data)
    print("generated test token:",token)
    return token
@app.route("/api/getPreference",methods=["POST"])
def getPreference():
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
        row=cursor.execute("SELECT USERID,COOKWARE,ALLERGICS FROM dbo.USER_PREFERENCE WHERE USERID=?",data['USERID']).fetchone()
        if(row is None):
            return errorReturn(404,"Not found")
        row.ALLERGICS=stringOperator.splitUnderscores(row.ALLERGICS)
        row.COOKWARE=stringOperator.splitUnderscores(row.COOKWARE)
        print(row)
        ret={
            "code":200,
            "message":"success",
            "data":{
                "USERID":row.USERID,
                "COOKWARE":row.COOKWARE,
                "ALLERGICS":row.ALLERGICS
            }
        }
        return ret

    return errorReturn(404,"Not found")
@app.route("/api/addOrUpdatePreference",methods=["POST"])
def addOrUpdatePreference():
    argsJson = request.data.decode('utf-8')
    argsJson = json.loads(argsJson)
    token=argsJson['token']
    data,expired,state,message=jwtTool.decodeToken(token)
    if(state==False):
        if(str(message)=="Signature has expired"):
            return errorReturn(400,str(message))
        return errorReturn(300,str(message))
    with get_conn() as conn:
        cursor = conn.cursor()
        row=cursor.execute("SELECT USERID,COOKWARE,ALLERGICS FROM dbo.USER_PREFERENCE WHERE USERID=?",data['USERID']).fetchone()
        if(row is None):
            sql = "INSERT INTO dbo.USER_PREFERENCE (USERID, COOKWARE,ALLERGICS) VALUES (?, ?, ?)"
            cookware=stringOperator.mergeUnderscores(argsJson['cookware'])
            allergics=stringOperator.mergeUnderscores(argsJson['allergics'])
            print(cookware)
            print(allergics)
            cursor.execute(sql, data['USERID'],cookware,allergics)
            conn.commit()
        else:
            sql = "UPDATE dbo.USER_PREFERENCE SET COOKWARE=?,ALLERGICS=?  WHERE USERID=?"
            cookware=stringOperator.mergeUnderscores(argsJson['cookware'])
            allergics=stringOperator.mergeUnderscores(argsJson['allergics'])
            print(cookware)
            print(allergics)
            cursor.execute(sql, cookware,allergics,data['USERID'])
            conn.commit()
        ret={
            "code":200,
            "message":"success",
            "data":{
            }
        }
        return ret
    return errorReturn(500,"Error occur")


    





    
if __name__ == '__main__':
    app.run()