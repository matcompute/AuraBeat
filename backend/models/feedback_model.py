# backend/models/feedback_model.py

from database.mongo_config import db
from datetime import datetime
import uuid

feedback_col = db["feedback"]


def submit_feedback(uid, music_id, rating, comment, liked):
    feedback = {
        "uid": uid,
        "music_id": music_id,
        "rating": int(rating) if rating is not None else None,  # ✅ Safe conversion
        "comment": comment or "",  # ✅ Fallback to empty string if None
        "liked": bool(liked),
        "timestamp": datetime.utcnow()
    }
    return feedback_col.insert_one(feedback)

def get_feedback_by_user(uid):
    return list(feedback_col.find({"uid": uid}).sort("timestamp", -1))

def get_feedback_by_music(music_id):
    return list(feedback_col.find({"music_id": music_id}).sort("timestamp", -1))
