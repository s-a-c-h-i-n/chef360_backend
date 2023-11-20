from models.UserPreference import UserPreference
from dbInstance import db
from models.Blocklist import TokenBlocklist
from _connection import get_conn
import pyodbc
class UserPreferenceRepo:

    def __init__(self) -> None:
        pass
    def getPreference(self,email):
        conn = get_conn()
        cursor = conn.cursor()
        preference = cursor.execute("SELECT E_MAIL, COOKWARE,ALLERGICS FROM dbo.USER_PREFERENCE WHERE E_MAIL=?",email).fetchone()

        if preference is not None:
            return True,preference
        else:
            return False,None

    def addPreference(self,email,cookware,allergics):

        conn = get_conn()
        cursor = conn.cursor() 
        cursor.execute("INSERT INTO dbo.USER_PREFERENCE(E_MAIL, COOKWARE,ALLERGICS) VALUES(?,?,?)", (email,cookware,allergics))
        conn.commit()
        return email

    def updatePreference(self,email,cookware,allergics):
        conn = get_conn()
        cursor = conn.cursor() 
        cursor.execute("UPDATE dbo.USER_PREFERENCE SET COOKWARE=? , ALLERGICS=? WHERE E_MAIL=?", (cookware,allergics,email))
        conn.commit()
        return True


        
