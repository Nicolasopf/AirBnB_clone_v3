#!/usr/bin/python3
'''build api routes'''
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.city import City
from models.state import State
from models.place import Place
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def list_places(city_id):
    ''' Return a json with all the places for cities objects '''
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def places_post(city_id):
    ''' Return a new Json object'''
    json_input = request.get_json()
    if json_input:
        if 'name' in json_input.keys():
            if storage.get(City, city_id):
                json_input['city_id'] = city_id
                new_obj = City(**json_input)
                new_obj.save()
                return jsonify(new_obj.to_dict()), 201
            abort(404)
        abort(400, "Missing name")
    abort(400, 'Not a JSON')


@app_views.route('/places/<place_id>', methods=['GET'])
def list_place(place_id):
    ''' Return a json with all the cities objects '''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def place_get(place_id):
    ''' Delte a place '''
    place = storage.get(Place, place_id)

    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>', methods=['PUT'])
def place_update(place_id):
    ''' Update a Place '''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
