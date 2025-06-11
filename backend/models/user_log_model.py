from database.mongo_config import db
from datetime import datetime

user_logs_col = db["user_logs"]

def log_user_action(uid, action, metadata=None):
    metadata = metadata or {}

    log = {
        "user_id": uid,
        "action": action,
        "meta": metadata,  # ✅ FIXED: was "metadata"
        "valence": metadata.get("valence"),
        "arousal": metadata.get("arousal"),
        "timestamp": datetime.utcnow()
    }

    user_logs_col.insert_one(log)

def get_user_logs():
    return list(user_logs_col.find().sort("timestamp", -1))
