#!/usr/bin/python3
"""
Module View Cities
new view for City objects that handles all
default RESTFul API actions
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def list_all_cities(state_id):
    """retrives all list of cities"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """retrieve a specific City using city id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ DELETE a City by using city_id """
    city = storage.get('City', city_id)
    if city:
        storage.delete(city)
        storage.save()
        return ({}), 200
    abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """create a new City object"""
    cty_name = request.get_json()
    if not storage.get('State', state_id):
        abort(404)
    if not cty_name:
        abort(400, {'Not a JSON'})
    elif 'name' not in cty_name:
        abort(400, {'Missing name'})
    cty_name['state_id'] = state_id
    new_city = City(**cty_name)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """update a City object"""
    if not request.is_json():
        abort(400, {'Not a JSON'})
    cityy = storage.get('City', city_id)
    if not cityy:
        abort(404)
    json = request.get_json()
    for key, value in json.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(cityy, key, value)
    storage.save()
    return jsonify(cityy.to_dict()), 200
