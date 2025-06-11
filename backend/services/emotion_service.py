import cv2
import numpy as np
import base64
from deepface import DeepFace
from datetime import datetime

EMOTION_MAPPINGS = {
    "happy": {"valence": 0.8, "arousal": 0.7},
    "sad": {"valence": -0.8, "arousal": 0.3},
    "angry": {"valence": -0.7, "arousal": 0.9},
    "neutral": {"valence": 0.0, "arousal": 0.5},
    "surprise": {"valence": 0.6, "arousal": 0.8},
    "fear": {"valence": -0.5, "arousal": 0.8},
    "disgust": {"valence": -0.7, "arousal": 0.6}
}

def decode_base64_image(image_base64):
    try:
        if 'base64,' in image_base64:
            image_base64 = image_base64.split('base64,')[1]
        image_bytes = base64.b64decode(image_base64)
        np_arr = np.frombuffer(image_bytes, np.uint8)
        return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    except Exception as e:
        print("❌ Image decoding failed:", e)
        return None

def detect_emotion_from_image(image_base64):
    try:
        if isinstance(image_base64, dict):
            return {"error": "Received dict instead of base64 string"}

        img = decode_base64_image(image_base64)
        if img is None:
            return {"error": "Invalid image data"}

        detectors = ['opencv', 'mtcnn', 'retinaface']
        result = None
        detector_used = None

        for detector in detectors:
            try:
                result = DeepFace.analyze(
                    img,
                    actions=["emotion"],
                    detector_backend=detector,
                    enforce_detection=True,
                    silent=True
                )
                if isinstance(result, list):
                    result = result[0]
                detector_used = detector
                break
            except Exception as e:
                print(f"⚠️ Detector {detector} failed:", e)
                continue

        if not result:
            return {"error": "No face detected. Try adjusting lighting or camera."}

        emotion = result["dominant_emotion"].lower()
        confidence = result["emotion"][emotion]

        if confidence < 0.4:
            print(f"❌ Low confidence for '{emotion}' ({confidence:.2f}) — skipping")
            return {"error": f"Low confidence ({confidence:.2f}) for emotion '{emotion}'"}

        mood = EMOTION_MAPPINGS.get(emotion, EMOTION_MAPPINGS["neutral"])

        print(f"✅ Detected emotion: {emotion} (confidence={confidence:.2f}, detector={detector_used})")

        return {
            "emotion": emotion,
            "valence": mood["valence"],
            "arousal": mood["arousal"],
            "timestamp": datetime.utcnow().isoformat(),
            "confidence": confidence,
            "detector": detector_used
        }

    except Exception as e:
        print(f"💥 Critical error:", e)
        return {"error": "Failed to analyze emotion. Internal error occurred."}
