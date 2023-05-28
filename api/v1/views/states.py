#!/usr/bin/python3

"""Module View States"""

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False)
def all_states():
    """retrieve list of all State objects """
    states = storage.all(State).values()
    states_list = [state.to_dict() for state in states]
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def retrieve_state(state_id):
    """retrieve a particular State using state id"""
    state = storage.all(State).values()
    state_obj = [obj.to_dict() for obj in state if obj.id == state_id]
    if state_obj == []:
        abort(404)
    return jsonify(state_obj[0])


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    '''Deletes a State object'''
    all_states = storage.all("State").values()
    state_obj = [obj.to_dict() for obj in all_states if obj.id == state_id]
    if state_obj == []:
        abort(404)
    state_obj.remove(state_obj[0])
    for obj in all_states:
        if obj.id == state_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def create_state():
    """ POST Method to create a State """
    state_name = request.get_json()
    if not state_name:
        abort(400, 'Not a JSON')
    if 'name' not in state_name:
        abort(400, 'Missing name')
    states = []
    new_state = State(name=request.json['name'])
    storage.new(new_state)
    storage.save()
    states.append(new_state.to_dict())
    return jsonify(states[0]), 201


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """ PUT Method to update a State """
    all_state = storage.all("State").values()
    state_obj = [obj.to_dict() for obj in all_state if obj.id == state_id]
    if state_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    state_obj[0]['name'] = request.json['name']
    for obj in all_state:
        if obj.id == state_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(state_obj[0]), 200
