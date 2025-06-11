# backend/models/music_model.py

from database.mongo_config import db
from datetime import datetime
import uuid

music_col = db["music"]

def add_music(title, genre, path, vibe, uploaded_by="admin"):
    track = {
        "music_id": str(uuid.uuid4()),
        "title": title,
        "genre": genre,
        "path": path,
        "vibe": vibe,
        "uploaded_by": uploaded_by,
        "created_at": datetime.utcnow()
    }
    return music_col.insert_one(track)

def get_music_by_vibe(vibe):
    return list(music_col.find({"vibe": vibe}))

def get_music_by_id(music_id):
    return music_col.find_one({"music_id": music_id})

def get_all_music():
    return list(music_col.find({}))
