#!/usr/bin/python3
"""
The above functions define routes for listing,
creating, updating, and deleting cities in a Flask
API.
"""
from flask import abort, jsonify, make_response, request
from api.v1.views import app_view
from models import storage, state, city


@app_view.route('/states/<id>/cities', strict_slashes=False)
def list_cities(id):
    if storage.get(state.State, id):
        state1 = storage.get(state.State, id)
    else:
        abort(404)

    return jsonify([city.to_dict() for city in state1.cities])


@app_view.route('/cities/<id>', strict_slashes=False)
def get_city(id):
    if storage.get(city.City, id):
        city1 = storage.get(city.City, id)
    else:
        abort(404)

    return jsonify(city1.to_dict())


@app_view.route('/cities/<id>', methods=['DELETE'], strict_slashes=False)
def delete_city_obj(id):
    if storage.get(city.City, id):
        city1 = storage.get(city.City, id)
    else:
        abort(404)
    storage.delete(city1)
    storage.save()
    return jsonify({})


@app_view.route('/states/<id>/cities', methods=['POST'], strict_slashes=False)
def create_city(id):
    try:
        obj = request.get_json()
    except Exception:
        return make_response(jsonify({'error': 'Not a json'}), 400)

    if storage.get(state.State, id):
        id = storage.get(state.State, id).id
    else:
        abort(404)

    obj['state_id'] = id

    if 'name' in obj.keys():
        new_city = city.City(**obj)
        new_city.save()
    else:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    return jsonify(new_city.to_dict()), 201


@app_view.route('/cities/<id>', methods=['PUT'], strict_slashes=False)
def update_city(id):
    if storage.get(city.City, id):
        new_city = storage.get(city.City, id)
    else:
        abort(404)

    try:
        obj_dict = request.get_json()
    except Exception:
        return make_response({'error': 'Not a json'}, 400)

    for key, value in obj_dict.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(new_city, key, value)
    new_city.save()

    return jsonify(new_city.to_dict())
