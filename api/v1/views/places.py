#!/usr/bin/python3
"""
The above functions define routes for listing,
getting, deleting, adding, and updating places in a
Flask application.
"""
from flask import Response, abort, jsonify, make_response, redirect, request
from api.v1.views import app_view
from models import place, storage, user
from models import city


@app_view.route('/cities/<id>/places', methods=['GET'], strict_slashes=False)
def list_places(id):
    if storage.get(city.City, id):
        city1 = storage.get(city.City, id)
    else:
        abort(404)

    return jsonify([obj.to_dict() for obj in city1.places])


@app_view.route('/places/<id>', strict_slashes=False)
def get_place(id):
    if storage.get(place.Place, id):
        obj = storage.get(place.Place, id)
    else:
        abort(404)
    return jsonify(obj.to_dict())


@app_view.route('/places/<id>', methods=['DELETE'], strict_slashes=False)
def delete_place(id):
    obj = storage.get(place.Place, id)
    if obj:
        storage.delete(obj)
        storage.save()
    else:
        abort(404)
    return jsonify({})


@app_view.route('/cities/<id>/places', methods=['POST'], strict_slashes=False)
def add_place(id):
    if storage.get(city.City, id):
        city_id = storage.get(city.City, id).id
    else:
        abort(404)

    try:
        obj = request.get_json()
    except Exception:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    if 'user_id' not in obj.keys():
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    elif 'name' not in obj.keys():
        return make_response(jsonify({'error': 'Missing name'}), 400)

    if not storage.get(user.User, obj['user_id']):
        abort(404)

    obj['city_id'] = city_id

    new_place = place.Place(**obj)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_view.route('/places/<id>', methods=['PUT'], strict_slashes=False)
def update_place(id):
    if storage.get(place.Place, id):
        place1 = storage.get(place.Place, id)
    else:
        abort(404)

    try:
        data = request.get_json()
    except Exception:
        return make_response(jsonify({'error': 'Not a json'}), 400)

    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place1, key, value)
    place1.save()

    return jsonify(place1.to_dict())
