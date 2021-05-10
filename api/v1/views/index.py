#!/usr/bin/python3
'''build api routes'''
from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.review import Review
from models.place import Place
from models.state import State
from models.city import City
from models import storage
from models.user import User


@app_views.route('/status')
def json_return():
    '''return a json with status'''
    return jsonify({'status': "OK"})


@app_views.route('/stats')
def return_num_objects():
    ''' Return the objects count '''
    classes = {"amenities": Amenity, "cities": City, "places": Place,
               "reviews": Review, "states": State, "users": User}
    counter_objects = {}
    for k, v in classes.items():
        counter_objects[k] = storage.count(v)

    return (jsonify(counter_objects))
