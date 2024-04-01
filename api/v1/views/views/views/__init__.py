#!/usr/bin/python3
'''
This code snippet is creating a Flask Blueprint
named `app_view` with the URL prefix `/api/v1`.
'''
from flask import Blueprint

app_view = Blueprint('app_view', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views import (states, cities, amenities,
                          users, places, places_reviews)
