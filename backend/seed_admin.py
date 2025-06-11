from database.mongo_config import db
import bcrypt

admin_email = "admin@aurabeat.com"
existing = db["users"].find_one({"email": admin_email})

if not existing:
    password = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt())
    db["users"].insert_one({
        "name": "Admin",
        "username": "admin",
        "email": admin_email,
        "password": password,
        "role": "admin",
        "status": "active"
    })
    print("✅ Admin account created")
else:
    # 🔁 Update role in case it was created without it
    db["users"].update_one({"email": admin_email}, {"$set": {"role": "admin"}})
    print("⚠️ Admin already existed — role updated to admin")
