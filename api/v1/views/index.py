#!/usr/bin/python3
"""
Status Route

This module defines a Flask route named "/status" that returns a JSON response
indicating the status of the application.
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def status():
    return jsonify(status="OK")

@app_views.route("/stats")
def stats():
    amenities_count = storage.count('Amenity')
    cities_count = storage.count('City')
    places_count = storage.count('Place')
    reviews_count = storage.count('Review')
    states_count = storage.count('State')
    users_count = storage.count('User')
    return jsonify(
        amenities=amenities_count,
        cities=cities_count,
        places=places_count,
        reviews=reviews_count,
        states=states_count,
        users=users_count
    )
