from flask import Blueprint
from services.openaiService import generateRecipe
from services.openaiService import getRecipe


openai_bp = Blueprint('openai_bp', __name__)

openai_bp.route('/generateRecipe', methods=['POST'])(generateRecipe)
