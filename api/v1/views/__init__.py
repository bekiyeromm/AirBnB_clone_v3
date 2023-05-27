#!/usr/bin/python3
from flask import Blueprint
# Create an instance of Blueprint with url prefix /api/v1
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
# import everything in the package api.v1.views.index
from api.v1.views.index import *
