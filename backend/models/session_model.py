# backend/models/session_model.py

from database.mongo_config import db
from datetime import datetime
import uuid

sessions_col = db["sessions"]

def start_session(uid):
    session = {
        "session_id": str(uuid.uuid4()),
        "uid": uid,
        "start_time": datetime.utcnow(),
        "end_time": None,
        "emotion_summary": {},
        "total_tracks_played": 0
    }
    sessions_col.insert_one(session)
    return session["session_id"]

def end_session(session_id, emotion_summary, total_tracks_played):
    return sessions_col.update_one(
        {"session_id": session_id},
        {
            "$set": {
                "end_time": datetime.utcnow(),
                "emotion_summary": emotion_summary,
                "total_tracks_played": total_tracks_played
            }
        }
    )

def get_sessions_by_user(uid):
    return list(sessions_col.find({"uid": uid}).sort("start_time", -1))
