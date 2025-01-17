#!/usr/bin/python3
'''build api routes'''
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.city import City
from models.state import State
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def list_cities(state_id):
    ''' return a json with all the cities for states objects '''
    if request.method == 'GET':
        state = storage.get(State, state_id)
        if not state:
            abort(404)
        list_objs = []

        for city in state.cities:
            list_objs.append(city.to_dict())
        return jsonify(list_objs)

    elif request.method == 'POST':
        json_input = request.get_json()
        if json_input:
            if 'name' in json_input.keys():
                if storage.get(State, state_id):
                    json_input['state_id'] = state_id
                    new_obj = City(**json_input)
                    new_obj.save()
                    return jsonify(new_obj.to_dict()), 201
                return abort(404)
            return abort(400, "Missing name")
        return abort(400, 'Not a JSON')


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
def list_city(city_id):
    ''' return a json with all the cities objects '''
    if request.method == 'GET':
        objects = storage.all(City)
        for obj in objects.items():
            city_obj = obj[1].to_dict()
            if city_obj['id'] == city_id:
                return jsonify(city_obj)
        return abort(404)
    if request.method == 'DELETE':
        objects = storage.all(City)
        for obj in objects.items():
            city_obj = obj[1].to_dict()
            if city_obj['id'] == city_id:
                storage.delete(obj[1])
                storage.save()
                return {}, 200
        return abort(404)
    if request.method == 'PUT':
        json_input = request.get_json()
        ignored_keys = ['id', 'state_id', 'created_at', 'updated_at']
        if json_input:
            city_obj = storage.get(City, city_id)
            if city_obj:
                for k, v in json_input.items():
                    if k not in ignored_keys:
                        setattr(city_obj, k, v)
                        city_obj.save()
                return jsonify(city_obj.to_dict()), 200
            return abort(404)
        return abort(400, 'Not a JSON')
