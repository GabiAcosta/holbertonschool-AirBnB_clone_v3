#!/usr/bin/python3
"""
Routes of endline of User
"""
from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.user import User


@app_views.route('/users', methods=['GET'])
def get_list_of_users():
    """List of all Users"""
    users = storage.all(User)
    user_list = [user.to_dict() for user in users.values()]
    return jsonify(user_list)


@app_views.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    """ Return a User object"""
    userObj = storage.get(User, user_id)
    if not userObj:
        return abort(404)
    else:
        return jsonify(userObj.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """ Delete a User"""
    userObj = storage.get(User, user_id)
    if not userObj:
        abort(404)
    else:
        storage.delete(userObj)
        storage.save()
        return jsonify({}), 200


@app_views.route("/users", methods=["POST"])
@app_views.route("/users/", methods=["POST"])
def create_user():
    """ Create a User"""
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    elif 'email' not in data:
        abort(400, 'Missing email')
    elif 'password' not in data:
        abort(400, 'Missing password')
    userIns = User(**data)
    userIns.save()
    return jsonify(userIns.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    userObj = storage.get(User, user_id)
    if not userObj:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for attr, value in data.items():
        if attr not in ["id", "email","created_at", "updated_at"]:
            setattr(userObj, attr, value)
    userObj.save()
    return jsonify(userObj.to_dict()), 200
