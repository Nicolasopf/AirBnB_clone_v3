#!/usr/bin/python3
from api.v1.views import app_views


@app_views.route('/status')
def json_return():
    return {"status": "OK"}