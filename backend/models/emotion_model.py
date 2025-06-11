from database.mongo_config import db
from models.user_model import find_user_by_uid
from datetime import datetime
import uuid

emotions_col = db["emotions"]

# Simple internal fallback mapping
def map_valence_arousal(emotion):
    mapping = {
        "happy": (0.8, 0.6),
        "sad": (-0.7, 0.4),
        "angry": (-0.6, 0.8),
        "fear": (-0.5, 0.7),
        "disgust": (-0.6, 0.6),
        "surprise": (0.4, 0.9),
        "neutral": (0.0, 0.1)
    }
    return mapping.get(emotion.lower(), (0.0, 0.0))

def log_emotion(uid, emotion, image_path, music_played, session_id=None, valence=None, arousal=None):
    # Auto-map valence/arousal if not provided
    if valence is None or arousal is None:
        valence, arousal = map_valence_arousal(emotion)

    entry = {
        "uid": uid,
        "timestamp": datetime.utcnow(),
        "emotion": emotion,
        "image_path": image_path,
        "music_played": music_played,
        "session_id": session_id or str(uuid.uuid4()),
        "valence": valence,
        "arousal": arousal
    }
    return emotions_col.insert_one(entry)

def get_user_emotions(uid):
    return list(emotions_col.find({"uid": uid}).sort("timestamp", -1))

def get_vibe_count_by_emotion(emotion):
    pipeline = [
        {"$match": {
            "emotion": emotion,
            "music_played": {"$ne": ""}
        }},
        {"$sort": {"timestamp": -1}},
        {"$group": {"_id": "$uid", "latest": {"$first": "$$ROOT"}}}
    ]

    recent_vibes = list(emotions_col.aggregate(pipeline))

    count = 0
    for record in recent_vibes:
        uid = record["_id"]
        user = find_user_by_uid(uid)
        if user and user.get("role") != "admin":
            count += 1

    return count
