#!/usr/bin/python3
"""
The function `count_obj` retrieves the count of objects
for each class in the `classes` dictionary
and returns the statistics in JSON format.
"""
from flask import jsonify
from api.v1.views import app_view
from models import storage
from models import state, amenity, city, place, review, user


classes = {
    'amenities': amenity.Amenity,
    'cities': city.City,
    'places': place.Place,
    'reviews': review.Review,
    'states': state.State,
    'users': user.User
}


@app_view.route('/status')
def status():
    return jsonify({'status': 'OK'}), 200


@app_view.route('/stats')
def count_obj():
    stat = {}
    for name, clas in classes.items():
        stat[name] = storage.count(clas)
    return jsonify(stat)
