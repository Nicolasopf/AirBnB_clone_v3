#!/usr/bin/python3
'''build api routes'''
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET', 'POST'])
def list_users():
    ''' return a json with all the users objects or update another one '''
    if request.method == 'GET':
        objects = storage.all(User)
        list_objs = []
        for obj in objects.items():
            list_objs.append(obj[1].to_dict())
        return jsonify(list_objs)
    elif request.method == 'POST':
        json_input = request.get_json()
        if json_input and 'name' in json_input.keys():
            user_obj = User(**json_input)
            user_obj.save()
            return jsonify(user_obj.to_dict()), 201
        elif json_input is None:
            return abort(400, 'Not a JSON')
        return abort(400, "Missing name")


@app_views.route('/users/<user_id>',
                 methods=['GET', 'DELETE', 'POST', 'PUT'])
def users_requests(user_id):
    ''' Get users by id, delete them, put a new one, and update. '''
    if request.method == 'GET':
        objects = storage.all(User)
        for obj in objects.items():
            if user_id == obj[1].id:
                return jsonify(obj[1].to_dict())
        return abort(404)
    elif request.method == 'DELETE':
        user_obj = storage.get(User, user_id)
        if user_obj:
            storage.delete(user_obj)
            storage.save()
            return jsonify({})
        return abort(404)
    elif request.method == 'PUT':
        json_input = request.get_json()
        if json_input is None:
            abort(400, 'Not a JSON')
        ignored_keys = ["id", "created_at", "updated_at"]
        user_obj = storage.get(User, user_id)
        if user_obj:
            for k, v in json_input.items():
                if k not in ignored_keys:
                    setattr(user_obj, k, v)
                    user_obj.save()
            return jsonify(user_obj.to_dict())
        return abort(404)
