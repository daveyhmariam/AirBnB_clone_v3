#!/usr/bin/python3
"""
The above functions define routes for managing reviews
in a Flask application, including listing,
getting, adding, updating, and deleting reviews.
"""
from flask import abort, jsonify, make_response, request
from api.v1.views import app_view
from models import place, review, storage, user


@app_view.route('/places/<id>/reviews', methods=['GET'], strict_slashes=False)
def list_reviews(id):
    if storage.get(place.Place, id):
        place1 = storage.get(place.Place, id)
    else:
        abort(404)

    return jsonify([obj.to_dict() for obj in place1.reviews])


@app_view.route('/reviews/<id>', strict_slashes=False)
def get_review(id):
    if storage.get(review.Review, id):
        obj = storage.get(review.Review, id)
    else:
        abort(404)
    return jsonify(obj.to_dict())


@app_view.route('/reviews/<id>', methods=['DELETE'], strict_slashes=False)
def delete_review(id):
    obj = storage.get(review.Review, id)
    if obj:
        storage.delete(obj)
        storage.save()
    else:
        abort(404)
    return jsonify({})


@app_view.route('/places/<id>/reviews', methods=['POST'], strict_slashes=False)
def add_review(id):
    if storage.get(place.Place, id):
        place_id = storage.get(place.Place, id).id
    else:
        abort(404)

    try:
        obj = request.get_json()
    except Exception:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    if 'user_id' not in obj.keys():
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    elif 'text' not in obj.keys():
        return make_response(jsonify({'error': 'Missing text'}), 400)

    if not storage.get(user.User, obj['user_id']):
        abort(404)

    obj['place_id'] = place_id

    new_review = review.Review(**obj)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_view.route('/reviews/<id>', methods=['PUT'], strict_slashes=False)
def update_review(id):
    if storage.get(review.Review, id):
        review1 = storage.get(review.Review, id)
    else:
        abort(404)

    try:
        data = request.get_json()
    except Exception:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(review1, key, value)
    review1.save()

    return jsonify(review1.to_dict())
