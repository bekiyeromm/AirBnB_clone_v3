#!/usr/bin/python3

"""Module View Places"""

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User
from models.place import Place
from models.city import City


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places_of_city(city_id):
    '''list all Place objects in city'''
    cities = storage.all("City").values()
    city = [x.to_dict() for x in cities if x.id == city_id]
    if city == []:
        abort(404)
    places = [y.to_dict() for y in storage.all("Place").values()
              if city_id == y.city_id]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def place(place_id):
    '''Retrieves a particular Place object based on place_id'''
    places = storage.all("Place").values()
    place = [x.to_dict() for x in places if x.id == place_id]
    if place == []:
        abort(404)
    return jsonify(place[0])


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    '''Deletes a particular place object based on place_id'''
    places = storage.all("Place").values()
    place = [x.to_dict() for x in places if x.id == place_id]
    if place == []:
        abort(404)
    place.remove(place[0])
    for y in places:
        if y.id == place_id:
            storage.delete(y)
            storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """create a Place object using a POST request
    to /api/v1/cities/<city_id>/places
    """
    cities = storage.all('City').values()
    city = [x.to_dict() for x in cities if x.id == city_id]
    if city == []:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    data = request.get_json()
    user_id = data.get('user_id')
    name = data.get('name')
    if not user_id:
        abort(400, "Missing user_id")
    users = storage.all('User').values()
    user = [y.to_dict() for y in users if y.id == user_id]
    if user == []:
        abort(404)
    if not name:
        abort(400, "Missing name")
    place = []
    new_place = Place(city_id=city_id, user_id=user_id, name=name)
    storage.new(new_place)
    storage.save()
    place.append(new_place.to_dict())
    return jsonify(place[0]), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    places = storage.all('Place').values()
    place = [x.to_dict() for x in places if x.id == place_id]
    if place == []:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    ignored_key = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignored_key:
            setattr(place, key, value)
    storage.save()
    place = place.to_dict()
    return jsonify(place[0]), 200
