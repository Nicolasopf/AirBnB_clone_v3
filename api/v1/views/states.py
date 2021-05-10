#!/usr/bin/python3
'''build api routes'''
from api.v1.views import app_views
from flask import jsonify
from models.state import State
from models import storage


@app_views.route('/states')
def list_states():
    ''' return a json with all the states objects '''
    objects = storage.all(State)
    list_objs = []
    dic = {}
    for obj in objects.items():
        list_objs.append(obj[1].to_dict())
    return jsonify(list_objs)


@app_views.route('/statass')
def return_num_states():
    ''' Return the objects count '''
    classes = {"amenities": Amenity, "cities": City, "places": Place,
               "reviews": Review, "states": State, "users": User}
    counter_objects = {}
    for k, v in classes.items():
        counter_objects[k] = storage.count(v)

    return (jsonify(counter_objects))
