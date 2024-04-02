#!/usr/bin/python3
"""
This Python script sets up a Flask web application with
error handling and a teardown function for
closing the database connection.
"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_view
import os
from flask_cors import CORS


app = Flask(__name__)

app.register_blueprint(app_view)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def tear_down(exception):
    '''close database connection'''
    storage.close()


@app.errorhandler(404)
def handler(e):
    '''404 handler'''
    return jsonify({'error': 'Not found'}), 404  # response


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST')
    port = os.getenv('HBNB_API_PORT')

    host = host if host else '0.0.0.0'
    port = int(port) if port else 5000
    app.run(host=host, port=port, threaded=True)
