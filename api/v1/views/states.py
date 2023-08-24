#!/usr/bin/python3
"""
States Routes

This module defines a set of Flask routes related to state information in a
RESTful API.
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route("/states", strict_slashes=False)
def all_states():
    """Returns a JSON response containing information about all states."""
    states = storage.all(State)
    state_list = [state.to_dict() for state in states.values()]
    return jsonify(state_list)


@app_views.route("/states/<state_id>", strict_slashes=False)
def state(state_id):
    """Returns a JSON response containing information about a specific
    state."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a state with the given ID."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """Creates a new state based on JSON data."""
    data = request.get_json(silent=True)
    if data is None:
        abort(400, 'Not a JSON')
    elif 'name' not in data:
        abort(400, 'Missing name')
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """Updates the information of a state with the given ID."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        for attr, value in data.items():
            if attr not in ["id", "state_id", "created_at", "updated_at"]:
                setattr(state, attr, value)
        state.save()
        return jsonify(state.to_dict()), 200
