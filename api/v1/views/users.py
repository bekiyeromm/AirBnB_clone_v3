#!/usr/bin/python3
"""user api for handling users"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def list_users():
    '''Retrieves all User objects'''
    users = [x.to_dict() for x in storage.all("User").values()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    '''Retrieves a particular User object based on user_id'''
    users = storage.all("User").values()
    user = [x.to_dict() for x in users if x.id == user_id]
    if user == []:
        abort(404)
    return jsonify(user[0])


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    '''Deletes a particular User object based on user_id'''
    users = storage.all("User").values()
    user = [x.to_dict() for x in users if x.id == user_id]
    if user == []:
        abort(404)
    user.remove(user[0])
    for y in users:
        if y.id == user_id:
            storage.delete(y)
            storage.save()
    return jsonify({}), 200


@app_views.route('/users/', methods=['POST'],
                 strict_slashes=False)
def create_user():
    '''Creates a new User object'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'email' not in request.get_json():
        abort(400, 'Missing email')
    if 'password' not in request.get_json():
        abort(400, 'Missing password')
    user = []
    new_user = User(email=request.json['email'],
                    password=request.json['password'])
    storage.new(new_user)
    storage.save()
    user.append(new_user.to_dict())
    return jsonify(user[0]), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def updates_user(user_id):
    '''Updates a User object using user_id'''
    users = storage.all("User").values()
    user = [x.to_dict() for x in users if x.id == user_id]
    if user == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    try:
        user[0]['first_name'] = request.json['first_name']
    except:
        pass
    try:
        user[0]['last_name'] = request.json['last_name']
    except:
        pass
    for y in users:
        if y.id == user_id:
            try:
                if request.json['first_name'] is not None:
                    y.first_name = request.json['first_name']
            except:
                pass
            try:
                if request.json['last_name'] is not None:
                    y.last_name = request.json['last_name']
            except:
                pass
    storage.save()
    return jsonify(user[0]), 200
