# backend/models/suggestion_model.py

from database.mongo_config import db
from datetime import datetime
import uuid

suggestions_col = db["suggestions"]

def save_suggestions(uid, suggested_music_ids, algorithm="default"):
    entry = {
        "uid": uid,
        "suggested_music_ids": suggested_music_ids,
        "generated_at": datetime.utcnow(),
        "algorithm": algorithm
    }
    return suggestions_col.insert_one(entry)

def get_latest_suggestions(uid):
    return suggestions_col.find_one({"uid": uid}, sort=[("generated_at", -1)])
