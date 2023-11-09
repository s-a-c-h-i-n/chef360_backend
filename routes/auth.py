from flask import Blueprint
from services.authService import login, logout

auth_bp = Blueprint('auth_bp', __name__)

auth_bp.route('/login', methods=['POST'])(login)
auth_bp.route('/logout', methods=['DELETE'])(logout)