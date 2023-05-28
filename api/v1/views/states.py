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
    """retrieve a particular State using id"""
    state = storage.get('State', state_id)
    if state:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ DELETE Method to delete a State """
    state = storage.get('State', state_id)
    if state:
        storage.delete(state)
        storage.save()
        return ({})
    abort(404)


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def create_state():
    """ POST Method to create a State """
    state_name = request.get_json()
    if not state_name:
        abort(400, 'Not a JSON')
    elif 'name' not in state_name:
        abort(400, 'Missing name')
    new_state = State(**state_name)
    new_state.save()
    return new_state.to_dict(), 201


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """ PUT Method to update a State """
    update_attr = request.get_json()
    if not update_attr:
        abort(400, {'Not a JSON'})
    my_state = storage.get('State', state_id)
    if not my_state:
        abort(404)
    for key, value in update_attr.items():
        setattr(my_state, key, value)
    storage.save()
    return jsonify(my_state.to_dict()), 200
