# backend/models/admin_log_model.py

from database.mongo_config import db
from datetime import datetime
import uuid

admin_logs_col = db["admin_logs"]

def log_admin_action(admin_uid, action, target_uid=None):
    entry = {
        "log_id": str(uuid.uuid4()),
        "admin_uid": admin_uid,
        "action": action,
        "target_uid": target_uid,
        "timestamp": datetime.utcnow()
    }
    return admin_logs_col.insert_one(entry)

def get_admin_logs(admin_uid=None):
    query = {"admin_uid": admin_uid} if admin_uid else {}
    return list(admin_logs_col.find(query).sort("timestamp", -1))
