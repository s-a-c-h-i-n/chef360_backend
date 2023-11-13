from flask import Blueprint
from services.authService import login
from services.authService import register
from services.authService import getPersonalInfor


auth_bp = Blueprint('auth_bp', __name__)

auth_bp.route('/login', methods=['POST'])(login)

auth_bp.route('/register', methods=['POST'])(register)

auth_bp.route('/getPersonalInfor', methods=['POST'])(getPersonalInfor)
