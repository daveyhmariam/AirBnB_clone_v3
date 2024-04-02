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


app = Flask(__name__)

app.register_blueprint(app_view)


@app.teardown_appcontext
def tear_down(exception):
    '''close database connection'''
    storage.close()


@app.errorhandler(404)
def handler(e):
    '''404 handler'''
    return jsonify({'error': 'Not found'}), 404  # response


if __name__ == '__main__':
    app.run(os.getenv('HBNB_API_HOST') or '0.0.0.0',
            os.getenv('HBNB_API_PORT') or 5000,
            threaded=True)
