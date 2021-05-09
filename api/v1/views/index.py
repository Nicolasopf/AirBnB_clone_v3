#!/usr/bin/python3
'''build api routes'''
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def json_return():
    '''return a json with status'''
    return jsonify({'status':"OK"})
