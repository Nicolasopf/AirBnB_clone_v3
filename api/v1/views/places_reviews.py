#!/usr/bin/python3
'''build api routes'''
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.city import City
from models.state import State
from models.place import Place
from models.review import Review
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def list_reviews(place_id):
    ''' Return a json with all the places for cities objects '''
    objects = storage.all(Review)
    list_objs = []
    for obj in objects.items():
        review_obj = obj[1].to_dict()
        if review_obj['place_id'] == place_id:
            list_objs.append(review_obj)
    if list_objs:
        return jsonify(list_objs)
    return abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def places_post(place_id):
    ''' Return a new Json object'''
    json_input = request.get_json()
    if json_input:
        if 'name' in json_input.keys():
            if storage.get(Place, place_id):
                json_input['place_id'] = place_id
                new_obj = Review(**json_input)
                new_obj.save()
                return jsonify(new_obj.to_dict()), 201
            return abort(404)
        return abort(400, "Missing name")
    return abort(400, 'Not a JSON')


@app_views.route('/places/<place_id>', methods=['GET'])
def list_city(place_id):
    ''' Return a json with all the cities objects '''
    objects = storage.all(Review)
    for obj in objects.items():
        place_obj = obj[1].to_dict()
        if place_obj['id'] == place_id:
            return jsonify(place_obj)
    return abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def place_get(place_id):
    ''' Delte a place '''
    objects = storage.all(Place)
    for obj in objects.items():
        place_obj = obj[1].to_dict()
        if place_obj['id'] == place_id:
            storage.delete(obj[1])
            storage.save()
            return jsonify({}), 200
    return abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'])
def place_update(place_id):
    ''' Update a Place '''
    json_input = request.get_json()
    objects = storage.all(Place)
    ignored_keys = ['id', 'place_id', 'created_at', 'updated_at']
    if json_input:
        for obj in objects.items():
            place_obj = obj[1]
            if place_obj.to_dict()['id'] == place_id:
                for k, v in json_input.items():
                    if k not in ignored_keys:
                        setattr(place_obj, k, v)
                        place_obj.save()
                return jsonify(place_obj.to_dict()), 200
        return abort(404)
    return abort(400, "Not a JSON")
