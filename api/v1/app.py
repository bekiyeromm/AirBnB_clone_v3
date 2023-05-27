#!/usr/bin/python3

"""flask app server"""

from os import getenv
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown_app(exception):
    """closes or handles the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def error_404(error):
    '''handler for 404 errors that returns a
    JSON-formatted 404 status code response
    content should be: error: Not found
    '''
    resp = jsonify({"error": "Not found"})
    resp.status_code = 404
    return resp


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    app.run(host=host, port=port, threaded=True)
