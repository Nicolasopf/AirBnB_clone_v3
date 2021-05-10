#!/usr/bin/python3
'''build api routes'''
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET', 'POST'])
def list_states():
    ''' return a json with all the states objects or update another one '''
    if request.method == 'GET':
        objects = storage.all(State)
        list_objs = []
        for obj in objects.items():
            list_objs.append(obj[1].to_dict())
        return jsonify(list_objs)
    elif request.method == 'POST':
        json_input = request.get_json()
        if json_input and 'name' in json_input.keys():
            state_obj = State(**json_input)
            state_obj.save()
            return jsonify(state_obj.to_dict()), 201
        elif json_input is None:
            return abort(400, 'Not a JSON')
        return abort(400, "Missing name")


@app_views.route('/states/<state_id>',
                 methods=['GET', 'DELETE', 'POST', 'PUT'])
def states_requests(state_id):
    ''' Get states by id, delete them, put a new one, and update. '''
    if request.method == 'GET':
        objects = storage.all(State)
        for obj in objects.items():
            if state_id == obj[1].id:
                return jsonify(obj[1].to_dict())
        return abort(404)
    elif request.method == 'DELETE':
        state_obj = storage.get(State, state_id)
        if state_obj:
            storage.delete(state_obj)
            storage.save()
            return jsonify({})
        return abort(404)
    elif request.method == 'PUT':
        json_input = request.get_json()
        if json_input is None:
            abort(400, 'Not a JSON')
        ignored_keys = ["id", "created_at", "updated_at"]
        state_obj = storage.get(State, state_id)
        if state_obj:
            for k, v in json_input.items():
                if k not in ignored_keys:
                    setattr(state_obj, k, v)
                    state_obj.save()
            return jsonify(state_obj.to_dict())
        return abort(404)
