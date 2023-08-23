#!/usr/bin/python3
"""
Status Route

This module defines a Flask route named "/status" that returns a JSON response
indicating the status of the application.
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    return jsonify(status="OK")
