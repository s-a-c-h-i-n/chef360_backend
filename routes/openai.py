from flask import Blueprint
from services.openaiService import generateRecipe, createRecipePrompt
from services.openaiService import getRecipe


openai_bp = Blueprint('openai_bp', __name__)

openai_bp.route('/generateRecipe', methods=['POST'])(generateRecipe)
openai_bp.route('/createRecipePrompt', methods=['GET'])(createRecipePrompt)
