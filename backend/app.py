from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from routes.route_emotion import route_emotion
from routes.route_user import route_user
from routes.route_admin import route_admin
from routes.route_feedback import route_feedback
from routes.route_music import route_music

app = Flask(__name__, static_folder="static")
CORS(app)

# 🔐 JWT Configuration
app.config["JWT_SECRET_KEY"] = "super-secret-key-change-this"  # Replace in production
jwt = JWTManager(app)

# 🔗 Register Routes
app.register_blueprint(route_emotion)
app.register_blueprint(route_user)
app.register_blueprint(route_admin)
app.register_blueprint(route_feedback)
app.register_blueprint(route_music)

@app.route("/")
def index():
    return {"message": "AuraBeat Flask Backend (MongoDB) is Live!"}, 200

if __name__ == "__main__":
    app.run(debug=True)
