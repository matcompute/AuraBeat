# backend/routes/route_feedback.py

from flask import Blueprint, request, jsonify
from database.mongo_config import db
from bson import ObjectId

from models.feedback_model import (
    submit_feedback,
    get_feedback_by_user,
    get_feedback_by_music
)
from models.user_log_model import log_user_action  # ✅ New import

route_feedback = Blueprint("route_feedback", __name__)

@route_feedback.route("/feedback", methods=["POST"])
def give_feedback():
    data = request.json
    uid = data.get("uid")
    music_id = data.get("music_id")
    rating = data.get("rating")  # Optional (can be null)
    comment = data.get("comment", "")
    liked = data.get("liked", False)

    if not uid or not music_id:
        return jsonify({"error": "Missing uid or music_id"}), 400

    submit_feedback(uid, music_id, rating, comment, liked)

    # ✅ Log the user action
    log_user_action(uid, "submitted feedback", {
        "music_id": music_id,
        "rating": rating,
        "comment": comment,
        "liked": liked
    })

    return jsonify({"message": "Feedback submitted"}), 201

@route_feedback.route("/feedback/user/<uid>", methods=["GET"])
def feedback_by_user(uid):
    result = get_feedback_by_user(uid)
    return jsonify(result), 200

@route_feedback.route("/feedback/music/<music_id>", methods=["GET"])
def feedback_by_music(music_id):
    result = get_feedback_by_music(music_id)
    return jsonify(result), 200

@route_feedback.route("/feedback/all", methods=["GET"])
def get_all_feedback():
    feedback = list(db["feedback"].find())
    for f in feedback:
        f["_id"] = str(f["_id"])
    return jsonify(feedback), 200
