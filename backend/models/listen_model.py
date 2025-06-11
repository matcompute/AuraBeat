# backend/models/listen_model.py

from database.mongo_config import db
from datetime import datetime
import uuid

listens_col = db["listens"]

def log_listen(uid, music_id, duration, emotion_at_play=None, session_id=None):
    entry = {
        "uid": uid,
        "music_id": music_id,
        "timestamp": datetime.utcnow(),
        "duration": int(duration),
        "emotion_at_play": emotion_at_play,
        "session_id": session_id or str(uuid.uuid4())
    }
    return listens_col.insert_one(entry)

def get_listens_by_user(uid):
    return list(listens_col.find({"uid": uid}).sort("timestamp", -1))

def get_listens_by_music(music_id):
    return list(listens_col.find({"music_id": music_id}))
