'''App module'''
import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.errorhandler(400)
def bad_request(error):
    """Error handler for a bad request"""
    return jsonify(dict(error='The Server did not understand' +
                                  'the request')), 400

@app.errorhandler(404)
def not_found(error):
    """Error handler for not found page"""
    return jsonify(dict(error='The Resource is not available')), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Error handler for wrong method to an endpoint"""
    return jsonify(dict(error='The HTTP request Method' +
                                  ' is not allowed')), 405

#To avoid circular imports
from app import views 
