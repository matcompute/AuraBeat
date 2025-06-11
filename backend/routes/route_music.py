from flask import Blueprint, request, jsonify
from models.music_model import (
    add_music,
    get_music_by_vibe,
    get_music_by_id,
    get_all_music
)
from models.listen_model import log_listen
from database.mongo_config import db
from datetime import datetime
from models.user_log_model import log_user_action

route_music = Blueprint("route_music", __name__)

# 🎵 Upload new music (admin only)
@route_music.route("/music", methods=["POST"])
def upload_music():
    data = request.json
    title = data.get("title")
    genre = data.get("genre")
    path = data.get("path")
    vibe = data.get("vibe")
    uploaded_by = data.get("uploaded_by", "admin")

    if not all([title, genre, path, vibe]):
        return jsonify({"error": "Missing fields"}), 400

    add_music(title, genre, path, vibe, uploaded_by)
    return jsonify({"message": "Music added"}), 201

# 🎧 Get music by vibe
@route_music.route("/music/vibe/<vibe>", methods=["GET"])
def music_by_vibe(vibe):
    uid = request.args.get("uid")
    tracks = get_music_by_vibe(vibe, uid)
    return jsonify(tracks), 200

# 🔍 Get music by ID
@route_music.route("/music/<music_id>", methods=["GET"])
def music_by_id(music_id):
    track = get_music_by_id(music_id)
    if not track:
        return jsonify({"error": "Track not found"}), 404
    return jsonify(track), 200

# 🎼 Get all music
@route_music.route("/music", methods=["GET"])
def all_music():
    tracks = get_all_music()
    return jsonify(tracks), 200

# 📥 Log a listening event
@route_music.route("/listen/log", methods=["POST"])
def log_listen_route():
    data = request.json
    uid = data.get("uid")
    music_id = data.get("music_id")
    duration = data.get("duration")
    emotion = data.get("emotion_at_play")
    session_id = data.get("session_id", None)
    valence = data.get("valence")
    arousal = data.get("arousal")

    print("🧪 [DEBUG] /listen/log received data:", {
        "uid": uid,
        "music_id": music_id,
        "duration": duration,
        "emotion": emotion,
        "valence": valence,
        "arousal": arousal,
        "session_id": session_id
    })

    if not all([uid, music_id is not None, duration]):
        return jsonify({"error": "Missing uid, music_id or duration"}), 400

    try:
        # Save to listens collection
        log_listen(uid, music_id, duration, emotion, session_id)

        # Save to user logs
        log_user_action(uid, "listened to track", {
            "music_id": music_id,
            "duration": duration,
            "emotion": emotion,
            "valence": valence,
            "arousal": arousal,
            "session_id": session_id
        })

        return jsonify({"message": "Listen logged"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# 📋 Get user’s playlist
@route_music.route("/playlist/<uid>", methods=["GET"])
def get_playlist(uid):
    playlist = list(db["playlist"].find({"user_id": uid}))
    for track in playlist:
        track["_id"] = str(track["_id"])
    return jsonify(playlist), 200

# 💾 Save to playlist
@route_music.route("/playlist/save", methods=["POST"])
def save_to_playlist():
    data = request.json
    uid = data.get("uid")
    track = data.get("track")

    if not uid or not track:
        return jsonify({"error": "Missing uid or track"}), 400

    track["user_id"] = uid
    db["playlist"].insert_one(track)

    log_user_action(uid, "saved to playlist", {
        "track": {
            "title": track.get("title"),
            "artist": track.get("artist"),
            "music_id": track.get("music_id")
        }
    })

    return jsonify({"message": "Saved to playlist"}), 201
