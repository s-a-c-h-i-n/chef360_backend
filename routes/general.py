from flask import Blueprint, render_template
from services.generalService import index

general_bp = Blueprint('general_bp', __name__)

@general_bp.route('/')
def landingPage():
    return index()
