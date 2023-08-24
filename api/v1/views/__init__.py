#!/usr/bin/python3
"""
Blueprint for API views.

This module defines a Flask Blueprint named "app_views" for organizing and
managing API endpoints.
"""
from flask import Blueprint


app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")
from api.v1.views.index import *
from api.v1.views.cities import *
