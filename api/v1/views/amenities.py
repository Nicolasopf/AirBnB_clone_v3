#!/usr/bin/python3
'''build api routes'''
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenities import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'])
def ameniy_get():
    ''' Return a json with all the amenities objects '''
    objects = storage.all(Amenity)
    list_objs = []
    for obj in objects.items():
        list_objs.append(obj[1].to_dict())
    return jsonify(list_objs)


@app_views.route('/amenities', methods=['POST'])
def amenity_post():
    json_input = request.get_json()
    if json_input and 'name' in json_input.keys():
        state_obj = Amenity(**json_input)
        state_obj.save()
        return jsonify(state_obj.to_dict()), 201
    elif json_input is None:
        return abort(400, 'Not a JSON')
    return abort(400, "Missing name")


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def amenities_get(amenity_id):
    ''' Get amenities by id '''
    objects = storage.all(Amenity)
    for obj in objects.items():
        if amenity_id == obj[1].id:
            return jsonify(obj[1].to_dict())
    return abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def amenities_delete(amenity_id):
    ''' Delete amenity '''
    state_obj = storage.get(Amenity, amenity_id)
    if state_obj:
        storage.delete(state_obj)
        storage.save()
        return jsonify({})
    return abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def amenity_put(amenity_id):
    ''' Update amenity '''
    json_input = request.get_json()
    if json_input is None:
        abort(400, 'Not a JSON')
    ignored_keys = ["id", "created_at", "updated_at"]
    state_obj = storage.get(Amenity, amenity_id)
    if state_obj:
        for k, v in json_input.items():
            if k not in ignored_keys:
                setattr(state_obj, k, v)
                state_obj.save()
        return jsonify(state_obj.to_dict())
    return abort(404)
