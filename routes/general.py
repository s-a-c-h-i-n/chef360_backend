from flask import Blueprint, render_template
from services.generalService import index
from services.generalService import register
from services.generalService import getPersonalInfor

general_bp = Blueprint('general_bp', __name__)

@general_bp.route('/')
def landingPage():
    return index()

@general_bp.route('/register')
def registerpage():
    return register()

@general_bp.route('/getPersonalInfor')
def getPersonalInfor():
    return getPersonalInfor()
