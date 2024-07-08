# app/routes.py
from flask import jsonify, request
from . import app
from .utils import get_location, get_temperature

@app.route('/api/hello', methods=['GET'])
def hello():
    # Your existing route logic using get_location and get_temperature
    pass

