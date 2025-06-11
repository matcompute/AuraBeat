from flask import Blueprint, request, jsonify, send_file
from database.mongo_config import db
from models.user_model import update_user_status, update_user_role, find_user_by_uid
from models.admin_log_model import log_admin_action
from models.user_log_model import get_user_logs
from bson import ObjectId

import csv
import io
import datetime

route_admin = Blueprint("route_admin", __name__)

# 🧍 All non-admin users
@route_admin.route("/admin/users", methods=["GET"])
def get_all_users():
    users = list(db["users"].find({"role": {"$ne": "admin"}}))
    for u in users:
        u["_id"] = str(u["_id"])
        u.pop("password", None)
    return jsonify(users), 200

# 🔍 Get user profile (basic only)
@route_admin.route("/admin/user/<uid>", methods=["GET"])
def get_user_detail(uid):
    user = find_user_by_uid(uid)
    if not user:
        return jsonify({"error": "User not found"}), 404
    user["_id"] = str(user["_id"])
    user.pop("password", None)
    return jsonify(user), 200

# ⚙️ Update user status
@route_admin.route("/admin/user/status", methods=["PATCH"])
def change_user_status():
    data = request.json
    uid = data.get("uid")
    status = data.get("status")
    admin_uid = data.get("admin_uid")
    if not all([uid, status, admin_uid]):
        return jsonify({"error": "Missing fields"}), 400
    update_user_status(uid, status)
    log_admin_action(admin_uid, f"set status to {status}", target_uid=uid)
    return jsonify({"message": "Status updated"}), 200

# 🔐 Update user role
@route_admin.route("/admin/user/role", methods=["PATCH"])
def change_user_role():
    data = request.json
    uid = data.get("uid")
    role = data.get("role")
    admin_uid = data.get("admin_uid")
    if not all([uid, role, admin_uid]):
        return jsonify({"error": "Missing fields"}), 400
    update_user_role(uid, role)
    log_admin_action(admin_uid, f"changed role to {role}", target_uid=uid)
    return jsonify({"message": "Role updated"}), 200

# 📊 Admin dashboard stats
@route_admin.route("/admin-stats", methods=["GET"])
def admin_stats():
    users = db["users"].count_documents({"role": {"$ne": "admin"}})
    emotions = db["emotions"].count_documents({})
    feedback = db["feedback"].count_documents({})
    listens = db["listens"].count_documents({})

    # Emotion breakdown
    pipeline = [{"$group": {"_id": "$emotion", "count": {"$sum": 1}}}]
    vibe_result = list(db["emotions"].aggregate(pipeline))
    vibe_counts = {v["_id"]: v["count"] for v in vibe_result}

    # 30s health snapshot
    threshold = datetime.datetime.utcnow() - datetime.timedelta(seconds=30)
    emotion_logs = db["emotions"].count_documents({"timestamp": {"$gte": threshold}})
    health = {
        "system": True,
        "emotion_logs": emotion_logs > 0
    }

    return jsonify({
        "user_count": users,
        "emotion_count": emotions,
        "feedback_count": feedback,
        "listen_count": listens,
        "vibe_counts": vibe_counts,
        "health": health
    }), 200

# 📜 Combined admin & user logs
@route_admin.route("/admin/logs", methods=["GET"])
def fetch_all_logs():
    admin_logs = list(db["admin_logs"].find().sort("timestamp", -1))
    user_logs = list(db["user_logs"].find().sort("timestamp", -1))

    for log in admin_logs:
        log["_id"] = str(log["_id"])
    for log in user_logs:
        log["_id"] = str(log["_id"])

    return jsonify({
        "admin_logs": admin_logs,
        "user_logs": user_logs
    }), 200

# 📤 Export user logs (JSON or CSV)
@route_admin.route("/admin/export-logs", methods=["GET"])
def export_user_logs():
    format = request.args.get("format", "json")
    logs = get_user_logs()

    if format == "csv":
        output = io.StringIO()
        fieldnames = ["user_id", "action", "valence", "arousal", "emotion", "timestamp"]
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()

        for log in logs:
            meta = log.get("meta", {})
            writer.writerow({
                "user_id": log.get("user_id", "N/A"),
                "action": log.get("action", ""),
                "valence": meta.get("valence", ""),
                "arousal": meta.get("arousal", ""),
                "emotion": meta.get("emotion", ""),
                "timestamp": log.get("timestamp", "")
            })

        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode()),
            mimetype="text/csv",
            as_attachment=True,
            download_name="user_logs.csv"
        )

    # fallback JSON
    for log in logs:
        log["_id"] = str(log["_id"])
    return jsonify(logs), 200

# 🧠 Full user activity (emotions, feedback, playlist)
@route_admin.route("/admin/user-activity/<uid>", methods=["GET"])
def get_user_activity(uid):
    user = find_user_by_uid(uid)
    if not user:
        return jsonify({"error": "User not found"}), 404

    emotions = list(db["emotions"].find({"uid": uid}).sort("timestamp", -1))
    feedback = list(db["feedback"].find({"uid": uid}).sort("timestamp", -1))
    playlist = list(db["playlist"].find({"uid": uid}))

    for item in emotions + feedback + playlist:
        item["_id"] = str(item["_id"])

    user["_id"] = str(user["_id"])
    user.pop("password", None)

    return jsonify({
        "user": user,
        "emotions": emotions,
        "feedback": feedback,
        "playlist": playlist
    }), 200

# 📚 User Sessions
@route_admin.route("/admin/user/<uid>/sessions", methods=["GET"])
def get_user_sessions(uid):
    from models.session_model import get_sessions_by_user
    sessions = get_sessions_by_user(uid)
    for s in sessions:
        s["_id"] = str(s["_id"])
    return jsonify(sessions), 200

# 🎯 Latest Suggestion for User
@route_admin.route("/admin/user/<uid>/suggestion", methods=["GET"])
def get_user_suggestion(uid):
    from models.suggestion_model import get_latest_suggestions
    suggestion = get_latest_suggestions(uid)
    if not suggestion:
        return jsonify({"message": "No suggestions found"}), 404
    suggestion["_id"] = str(suggestion["_id"])
    return jsonify(suggestion), 200
