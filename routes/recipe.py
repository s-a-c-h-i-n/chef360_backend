from flask import Blueprint
from services.recipeService import recipePromptGeneration,storeRecipe,getRecipe


recipe_bp = Blueprint('recipe_bp', __name__)


recipe_bp.route("/storeRecipe",methods=['POST'])(storeRecipe)
recipe_bp.route("/getRecipe",methods=['GET'])(getRecipe)
