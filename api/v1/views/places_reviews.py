#!/usr/bin/python3
"""places_reviews"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews/', methods=['GET'],
                 strict_slashes=False)
def reviews_of_place(place_id):
    '''lists of all Review objects of a Place '''
    places = storage.all("Place").values()
    place = [x.to_dict() for x in places if x.id == place_id]
    if place == []:
        abort(404)
    reviews = [y.to_dict() for y in storage.all("Review").values()
               if y.place_id == place_id]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    '''Retrieves a particular Review object '''
    reviews = storage.all("Review").values()
    review = [x.to_dict() for x in reviews if x.id == review_id]
    if review == []:
        abort(404)
    return jsonify(review[0])


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    '''Creates a new Review object'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'user_id' not in request.get_json():
        abort(400, 'Missing user_id')
    user_id = request.json['user_id']
    if 'text' not in request.get_json():
        abort(400, 'Missing text')
    places = storage.all("Place").values()
    place = [x.to_dict() for x in places if x.id == place_id]
    if place == []:
        abort(404)
    users = storage.all("User").values()
    user = [y.to_dict() for y in users if y.id == user_id]
    if user == []:
        abort(404)
    reviews = []
    new_review = Review(text=request.json['text'], place_id=place_id,
                        user_id=user_id)
    new_review.save()
    reviews.append(new_review.to_dict())
    return jsonify(reviews[0]), 201


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    '''Deletes a Review object based in review_id'''
    reviews = storage.all("Review").values()
    review = [x.to_dict() for x in reviews if x.id == review_id]
    if review == []:
        abort(404)
    for y in reviews:
        if y.id == review_id:
            storage.delete(y)
            storage.save()
    return jsonify({}), 200


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    '''Updates a Review object using review_id'''
    reviews = storage.all("Review").values()
    review = [x.to_dict() for x in reviews if x.id == review_id]
    if review == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in request.get_json().items():
        if key in ignore_keys:
            continue
        else:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
