# backend/models/playlist_model.py

from database.mongo_config import db
from datetime import datetime
import uuid

playlists_col = db["playlists"]

def create_playlist(uid, title, description="", is_public=True):
    playlist = {
        "playlist_id": str(uuid.uuid4()),
        "uid": uid,
        "title": title,
        "description": description,
        "track_ids": [],
        "created_at": datetime.utcnow(),
        "is_public": bool(is_public)
    }
    return playlists_col.insert_one(playlist)

def add_track_to_playlist(playlist_id, music_id):
    return playlists_col.update_one(
        {"playlist_id": playlist_id},
        {"$addToSet": {"track_ids": music_id}}
    )

def remove_track_from_playlist(playlist_id, music_id):
    return playlists_col.update_one(
        {"playlist_id": playlist_id},
        {"$pull": {"track_ids": music_id}}
    )

def get_playlists_by_user(uid):
    return list(playlists_col.find({"uid": uid}))

def get_public_playlists():
    return list(playlists_col.find({"is_public": True}))
