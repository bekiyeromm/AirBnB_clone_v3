#!/usr/bin/python3
'''flask app'''

from os import getenv
from flask import Flask
from models import storage
from api.v1.views import app_views

app = flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_app(exception):
    """closes or handles the storage on teardown"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
