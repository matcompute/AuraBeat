# backend/models/user_model.py

from database.mongo_config import db
from bson import ObjectId
import bcrypt
import uuid
from datetime import datetime

users_col = db["users"]

def create_user(name, username, email, password, role="user"):
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = {
        "uid": str(uuid.uuid4()),
        "name": name,
        "username": username,
        "email": email,
        "password": hashed_pw,
        "role": role,
        "status": "active",
        "online": False,
        "created_at": datetime.utcnow(),
        "last_login": None
    }
    result = users_col.insert_one(user)
    return str(result.inserted_id)

def find_user_by_email(email):
    return users_col.find_one({"email": email})

def find_user_by_uid(uid):
    return users_col.find_one({"uid": uid})

def verify_password(input_password, hashed_password):
    return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password)

def update_login_status(uid, online=True):
    update_fields = {"online": online}
    if online:
        update_fields["last_login"] = datetime.utcnow()
    return users_col.update_one({"uid": uid}, {"$set": update_fields})

def update_user_status(uid, status):
    return users_col.update_one({"uid": uid}, {"$set": {"status": status}})

def update_user_role(uid, role):
    return users_col.update_one({"uid": uid}, {"$set": {"role": role}})
def get_user_role(uid):
    user = users_col.find_one({"uid": uid})
    return user.get("role", "user") if user else "user"
