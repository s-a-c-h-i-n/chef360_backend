
from dbInstance import db
from models.Blocklist import TokenBlocklist
from _connection import get_conn
import pyodbc
class RecipeRepo:

    def __init__(self) -> None:
        pass

    def addRecipe(self,email,recipe):

        conn = get_conn()
        cursor = conn.cursor() 
        cursor.execute("INSERT INTO dbo.RECIPE(E_MAIL, RECIPEINFO) VALUES(?,?)", (email,recipe))
        conn.commit()
        return email

    def getRecipe(self,email):
        conn = get_conn()
        cursor = conn.cursor()
        recipes = cursor.execute("SELECT RECIPEINFO FROM dbo.RECIPE WHERE E_MAIL=?",email).fetchall()

        if recipes is not None:
            return True,recipes
        else:
            return False,None


        
