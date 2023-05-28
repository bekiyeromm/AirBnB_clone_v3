#!/usr/bin/python3
"""amenities"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities/', methods=['GET'])
def list_all_amenities():
    '''Retrieves a list of all Amenity objects'''
    amenity = [x.to_dict() for x in storage.all("Amenity").values()]
    return jsonify(amenity)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    '''Retrieves a specific Amenity object'''
    amenities = storage.all("Amenity").values()
    amenity = [x.to_dict() for x in amenities
               if x.id == amenity_id]
    if amenity == []:
        abort(404)
    return jsonify(amenity[0])


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    '''Deletes an Amenity object based on amnity_id'''
    amenities = storage.all("Amenity").values()
    amenity = [x.to_dict() for x in amenities
               if x.id == amenity_id]
    if amenity == []:
        abort(404)
    amenity.remove(amenity[0])
    for y in amenities:
        if y.id == amenity_id:
            storage.delete(y)
            storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/', methods=['POST'])
def create_amenity():
    '''Create new Amenity'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    amenities = []
    new_amenity = Amenity(name=request.json['name'])
    storage.new(new_amenity)
    storage.save()
    amenities.append(new_amenity.to_dict())
    return jsonify(amenities[0]), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def updates_amenity(amenity_id):
    '''Updates an Amenity object using amenity_id'''
    amenities = storage.all("Amenity").values()
    amenity = [x.to_dict() for x in amenities
               if x.id == amenity_id]
    if amenity == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    amenity[0]['name'] = request.json['name']
    for y in amenities:
        if y.id == amenity_id:
            y.name = request.json['name']
    storage.save()
    return jsonify(amenity[0]), 200
