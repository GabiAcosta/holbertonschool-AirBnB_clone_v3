#!/usr/bin/python3
"""
Routes of endline of place's reviews.
"""
from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_list_of_reviews(place_id):
    """List of reviews vinculed with a place"""
    reviews_list = []
    placeIns = storage.get(Place, place_id)
    if not placeIns:
        abort(404)
    for review in placeIns.reviews:
        reviews_list.append(review.to_dict())
    return jsonify(reviews_list)


@app_views.route("/reviews/<review_id>", methods=["GET"])
def get_review(review_id):
    """ Return a Review object"""
    reviewObj = storage.get(Review, review_id)
    if not reviewObj:
        return abort(404)
    else:
        return jsonify(reviewObj.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"])
def delete_review(review_id):
    """ Delete a Review object"""
    reviewObj = storage.get(Review, review_id)
    if not reviewObj:
        abort(404)
    else:
        storage.delete(reviewObj)
        storage.save()
        return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"])
@app_views.route("/places/<place_id>/reviews/", methods=["POST"])
def create_review(place_id):
    """ Create a Review object"""
    placeIns = storage.get(Place, place_id)
    if placeIns is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    elif 'text' not in data:
        abort(400, 'Missing text')
    elif "user_id" not in data:
        abort(400, "Missing user_id")
    user_id = storage.get(User, data["user_id"])
    if user_id is None:
        abort(404)
    data["place_id"] = place_id
    reviewIns = Review(**data)
    reviewIns.save()
    return jsonify(reviewIns.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    reviewObj = storage.get(Review, review_id)
    if not reviewObj:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for attr, value in data.items():
        if attr not in ["id", "user_id", "place_id", "created_at",
                        "updated_at"]:
            setattr(reviewObj, attr, value)
    reviewObj.save()
    return jsonify(reviewObj.to_dict()), 200
