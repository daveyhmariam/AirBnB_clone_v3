#!/usr/bin/python3
"""
This Python code defines routes for listing, getting,
creating, updating, and deleting user objects
in a Flask API.
"""
from api.v1.views import app_view
from flask import abort, request, jsonify, make_response
from models import storage, user


@app_view.route('/users', strict_slashes=False)
def list_of_users():
    return jsonify(
        [obj.to_dict()
         for obj in storage.all(user.User).values()]
    )


@app_view.route('/users/<id>', strict_slashes=False)
def get_user(id):
    if storage.get(user.User, id):
        amenity1 = storage.get(user.User, id)
    else:
        abort(404)

    return jsonify(amenity1.to_dict())


@app_view.route('/users/<id>', methods=['DELETE'], strict_slashes=False)
def delete_user(id):
    if storage.get(user.User, id):
        user1 = storage.get(user.User, id)
    else:
        abort(404)
    storage.delete(user1)
    storage.save()
    return jsonify({})


@app_view.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    try:
        obj = request.get_json()
    except Exception:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    if 'email' not in obj.keys():
        return make_response(jsonify({'error': 'Missing email'}), 400)
    elif 'password' not in obj.keys():
        return make_response(jsonify({'error': 'Missing password'}), 400)

    new_user = user.User(**obj)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_view.route('/users/<id>', methods=['PUT'], strict_slashes=False)
def update_user(id):
    if storage.get(user.User, id):
        new_user = storage.get(user.User, id)
    else:
        abort(404)

    try:
        obj_dict = request.get_json()
    except Exception:
        return make_response({'error': 'Not a JSON'}, 400)

    for key, value in obj_dict.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(new_user, key, value)
    new_user.save()

    return jsonify(new_user.to_dict())
