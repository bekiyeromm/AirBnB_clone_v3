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
    states = storage.all("State").values()

    state = [x.to_dict() for x in states if x.id == state_id]
    if state == []:
        abort(404)
    cities = [y.to_dict() for y in storage.all("City").values()
              if state_id == y.state_id]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """retrieve a specific City using city id"""
    cities = storage.all("City").values()
    city = [x.to_dict() for x in cities if x.id == city_id]
    if city == []:
        abort(404)
    return jsonify(city[0])


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ DELETE a City by using city_id """
    cities = storage.all("City").values()
    city = [x.to_dict() for x in cities if x.id == city_id]
    if city == []:
        abort(404)
    city.remove(city[0])
    for x in cities:
        if (x.id == city_id):
            storage.delete(x)
            storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_new_city(state_id):
    """create a new City object"""
    cty_name = request.get_json()
    if not cty_name:
        abort(400, {'Not a JSON'})
    if 'name' not in cty_name:
        abort(400, {'Missing name'})
    states = storage.all("State").values()
    state = [x.to_dict() for x in states if x.id == state_id]
    if state == []:
        abort(404)
    city = []
    new_city = City(name=request.json['name'], state_id=state_id)
    storage.new(new_city)
    storage.save()
    city.append(new_city.to_dict())
    return jsonify(city[0]), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """update a City object"""
    if not request.get_json():
        abort(400, {'Not a JSON'})
    cities = storage.all('City').values()
    city = [x.to_dict() for x in cities if x.id == city_id]
    if city == []:
        abort(404)
    city[0]['name'] = request.json['name']
    for x in cities:
        if x.id == city_id:
            x.name = request.json['name']
    storage.save()
    return jsonify(city[0]), 200
