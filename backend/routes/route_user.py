# backend/routes/route_user.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.user_model import (
    create_user,
    find_user_by_email,
    find_user_by_uid,
    verify_password,
    update_login_status
)

route_user = Blueprint("route_user", __name__)

@route_user.route("/register", methods=["POST"])
def register():
    data = request.json
    name = data.get("name")
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    if not all([name, username, email, password]):
        return jsonify({"error": "Missing fields"}), 400

    existing = find_user_by_email(email)
    if existing:
        return jsonify({"error": "Email already registered"}), 409

    inserted_id = create_user(name, username, email, password)
    return jsonify({"message": "User created", "id": inserted_id}), 201

@route_user.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not all([email, password]):
        return jsonify({"error": "Missing email or password"}), 400

    user = find_user_by_email(email)
    if not user or not verify_password(password, user.get("password")):
        return jsonify({"error": "Invalid credentials"}), 401

    update_login_status(user["uid"], online=True)

    # ✅ Generate JWT token
    access_token = create_access_token(identity=user["uid"])

    return jsonify({
        "token": access_token,
        "uid": user["uid"],
        "name": user.get("name"),
        "username": user.get("username"),
        "email": user.get("email"),
        "role": user.get("role"),
        "status": user.get("status"),
        "online": True,
        "last_login": user.get("last_login")
    }), 200

@route_user.route("/logout", methods=["POST"])
def logout():
    data = request.json
    uid = data.get("uid")
    if not uid:
        return jsonify({"error": "Missing uid"}), 400

    user = find_user_by_uid(uid)
    if not user:
        return jsonify({"error": "User not found"}), 404

    update_login_status(uid, online=False)
    return jsonify({"message": "Logged out"}), 200

@route_user.route("/profile/<uid>", methods=["GET"])
def profile(uid):
    user = find_user_by_uid(uid)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "uid": user["uid"],
        "name": user.get("name"),
        "username": user.get("username"),
        "email": user.get("email"),
        "role": user.get("role"),
        "status": user.get("status"),
        "online": user.get("online"),
        "created_at": user.get("created_at"),
        "last_login": user.get("last_login")
    }), 200
