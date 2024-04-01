#!/usr/bin/python3
"""
The above functions define routes for CRUD operations
on State objects in a Flask application.
"""
from flask import Response, abort, jsonify, make_response, redirect, request
from api.v1.views import app_view
from models import storage
from models.state import State


@app_view.route('/states', methods=['GET'], strict_slashes=False)
def list_states():
    result = []
    for state in storage.all(State).values():
        result.append(state.to_dict())
    return jsonify(result)


@app_view.route('/states/<id>', strict_slashes=False)
def get_state(id):
    if storage.get(State, id):
        obj = storage.get(State, id)
    else:
        abort(404)
    return jsonify(obj.to_dict())


@app_view.route('/states/<id>', methods=['DELETE'], strict_slashes=False)
def delete_obj(id):
    obj = storage.get(State, id)
    if obj:
        storage.delete(obj)
        storage.save()
    else:
        abort(404)
    return jsonify({})


@app_view.route('/states', methods=['POST'], strict_slashes=False)
def add_obj():
    try:
        obj = request.get_json()
    except Exception:
        return make_response(jsonify({'error': 'Not a json'}), 400)

    if 'name' in obj.keys():
        new_state = State(**obj)
        new_state.save()
    else:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    return jsonify(new_state.to_dict()), 201


@app_view.route('/states/<id>', methods=['PUT'], strict_slashes=False)
def update(id):
    if storage.get(State, id):
        state2 = storage.get(State, id)
    else:
        abort(404)

    try:
        data = request.get_json()
    except Exception:
        return make_response(jsonify({'error': 'Not a json'}), 400)

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state2, key, value)
    state2.save()

    return jsonify(state2.to_dict())
