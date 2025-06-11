from flask import Blueprint, request, jsonify
from models.emotion_model import log_emotion, get_user_emotions, get_vibe_count_by_emotion
from services.emotion_service import detect_emotion_from_image
from bson import ObjectId

route_emotion = Blueprint("route_emotion", __name__)

def serialize_object_ids(obj):
    if isinstance(obj, list):
        return [serialize_object_ids(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: serialize_object_ids(v) for k, v in obj.items()}
    elif isinstance(obj, ObjectId):
        return str(obj)
    else:
        return obj

@route_emotion.route("/detect-emotion", methods=["POST"])
def detect_emotion():
    try:
        data = request.get_json(force=True)
        print("📥 /detect-emotion received:", data)

        image = data.get("image")
        if not image or not isinstance(image, str):
            return jsonify({"error": "Image data must be a base64 string"}), 400

        result = detect_emotion_from_image(image)
        return jsonify(result), 200
    except Exception as e:
        print(f"Error in /detect-emotion: {e}")
        return jsonify({"error": "Server error in emotion detection"}), 500

@route_emotion.route("/log-emotion", methods=["POST"])
def log_user_emotion():
    data = request.json
    uid = data.get("uid")
    emotion = data.get("emotion")
    image_path = data.get("image_path", "")
    music_played = data.get("music_played", "")
    session_id = data.get("session_id", None)
    valence = data.get("valence", None)
    arousal = data.get("arousal", None)

    if not all([uid, emotion]):
        return jsonify({"error": "Missing fields"}), 400

    log_emotion(uid, emotion, image_path, music_played, session_id, valence, arousal)
    return jsonify({"message": "Emotion logged"}), 201

@route_emotion.route("/user-emotions/<uid>", methods=["GET"])
def fetch_user_emotions(uid):
    emotions = get_user_emotions(uid)
    emotions = serialize_object_ids(emotions)
    return jsonify(emotions), 200

@route_emotion.route("/vibe-count/<emotion>", methods=["GET"])
def get_vibe_count_route(emotion):
    count = get_vibe_count_by_emotion(emotion)
    return jsonify({"emotion": emotion, "count": count}), 200
