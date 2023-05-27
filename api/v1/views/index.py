#!/usr/bin/python3
'''status of api'''

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    '''returns a JSON string: "status": "OK"'''
    return jsonfy(status": "OK")
