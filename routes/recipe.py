from flask import Blueprint
from services.recipeService import recipePromptGeneration,storeRecipe


recipe_bp = Blueprint('recipe_bp', __name__)

recipe_bp.route('/recipePrompt', methods=['POST'])(recipePromptGeneration)
recipe_bp.route("/storeRecipe",methods=['POST'])(storeRecipe)