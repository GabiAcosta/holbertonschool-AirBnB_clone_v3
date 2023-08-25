#!/usr/bin/python3
"""
Routes of endline of Place
"""
from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.city import City
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_list_of_places(city_id):
    """List of all places"""
    places_list = []
    cityIns = storage.get(City, city_id)
    if not cityIns:
        abort(404)
    for place in cityIns.places:
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route("/places/<place_id>", methods=["GET"])
def get_place(place_id):
    """ Return a Place object"""
    placeObj = storage.get(Place, place_id)
    if not placeObj:
        return abort(404)
    else:
        return jsonify(placeObj.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"])
def delete_place(place_id):
    """ Delete a place object"""
    placeObj = storage.get(Place, place_id)
    if not placeObj:
        abort(404)
    else:
        storage.delete(placeObj)
        storage.save()
        return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"])
@app_views.route("/cities/<city_id>/places/", methods=["POST"])
def create_place(city_id):
    """ Create a Place object"""
    cityIns = storage.get(City, city_id)
    if cityIns is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    elif 'name' not in data:
        abort(400, 'Missing name')
    elif 'user_id' not in data:
        abort(400, 'Missing user_id')
    data["city_id"] = city_id
    placeIns = Place(**data)
    placeIns.save()
    return jsonify(placeIns.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    placeObj = storage.get(Place, place_id)
    if not placeObj:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for attr, value in data.items():
        if attr not in ["id", "user_id", "city_id","created_at", "updated_at"]:
            setattr(placeObj, attr, value)
    placeObj.save()
    return jsonify(placeObj.to_dict()), 200
