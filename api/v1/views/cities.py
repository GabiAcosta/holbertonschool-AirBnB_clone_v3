#!/usr/bin/python3
"""
Routes of endline of City
"""
from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_list_of_cities(state_id):
    """List of cities vinculed with a state_id"""
    stateIns = storage.get(State, state_id)
    if not stateIns:
        return abort(404)
    city_storage = storage.all(City)
    city_list = []
    for obj in city_storage:
        cityIns = storage.get(City, (obj.split(".")[1]))
        if cityIns.state_id == stateIns.id:
            city_list.append(cityIns.to_dict())
    return jsonify(city_list)


@app_views.route("/cities/<city_id>", methods=["GET"])
def get_city(city_id):
    """ Return a city object"""
    cityObj = storage.get(City, city_id)
    if not cityObj:
        return abort(404)
    else:
        return jsonify(cityObj.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    """ Delete a city object"""
    cityObj = storage.get(City, city_id)
    if not cityObj:
        return abort(404)
    else:
        storage.delete(cityObj)
        return 200, {}


@app_views.route("/api/v1/states/<state_id>/cities", methods=["POST"])
def create_city(state_id):
    """ Create a city object"""
    data = request.get_json()
    if not data:
        return jsonify('Not a JSON'), 400
    elif 'name' not in data:
        return jsonify('Missing name'), 400
    else:
        stateIns = storage.get(State, state_id)
        if not stateIns:
            return abort(404)
        cityIns = City()
        cityIns.state_id = state_id
        cityIns.save()
        return jsonify(cityIns.to_dict), 201


@app_views.route("/api/v1/cities/<city_id>", methods=["PUT"])
def update_city(city_id):
    cityObj = storage.get(City, city_id)
    if not cityObj:
        return abort(404)
    else:
        data = request.get_json()
        if not data:
            return jsonify('Not a JSON'), 400
        for attr, value in data.items():
            if attr not in ["id", "state_id", "created_at", "updated_at"]:
                setattr(cityObj, attr, value)
        cityObj.save()
        return jsonify(cityObj.to_dict), 200
