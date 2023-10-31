
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import render_template, request, jsonify, session, send_from_directory, Flask
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://'
db = SQLAlchemy(app)
