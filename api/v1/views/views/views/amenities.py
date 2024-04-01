#!/usr/bin/python3
"""
The above functions define routes for CRUD operations
on Amenity objects in a Flask API. from flask import abort,
jsonify, make_response, request
"""
from flask import abort, jsonify, make_response, request
from api.v1.views import app_view
from models import storage, amenity


@app_view.route('/amenities', strict_slashes=False)
def list_of_amenities():
    return jsonify(
        [obj.to_dict()
         for obj in storage.all(amenity.Amenity).values()]
    )


@app_view.route('/amenities/<id>', strict_slashes=False)
def get_amenitiy(id):
    if storage.get(amenity.Amenity, id):
        amenity1 = storage.get(amenity.Amenity, id)
    else:
        abort(404)

    return jsonify(amenity1.to_dict())


@app_view.route('/amenities/<id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(id):
    if storage.get(amenity.Amenity, id):
        amenity1 = storage.get(amenity.Amenity, id)
    else:
        abort(404)
    storage.delete(amenity1)
    storage.save()
    return jsonify({})


@app_view.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    try:
        obj = request.get_json()
    except Exception:
        return make_response(jsonify({'error': 'Not a json'}), 400)

    if 'name' in obj.keys():
        new_amenity = amenity.Amenity(**obj)
        new_amenity.save()
    else:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    return jsonify(new_amenity.to_dict()), 201


@app_view.route('/amenities/<id>', methods=['PUT'], strict_slashes=False)
def update_amenity(id):
    if storage.get(amenity.Amenity, id):
        new_amenity = storage.get(amenity.Amenity, id)
    else:
        abort(404)

    try:
        obj_dict = request.get_json()
    except Exception:
        return make_response({'error': 'Not a json'}, 400)

    for key, value in obj_dict.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(new_amenity, key, value)
    new_amenity.save()

    return jsonify(new_amenity.to_dict())
