import cv2
from deepface import DeepFace

detector_backend = "retinaface"
cap = cv2.VideoCapture(0)

print("[INFO] Starting multi-person emotion detection... Press 'q' to quit.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    if isinstance(frame, tuple):
        print("[ERROR] Frame is a tuple, not an image.")
        continue

    try:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = DeepFace.analyze(
            rgb_frame,
            actions=["emotion", "age", "gender"],
            detector_backend=detector_backend,
            enforce_detection=False
        )

        if not isinstance(results, list):
            results = [results]

        for res in results:
            region = res.get("region", {})
            x, y, w, h = region.get("x", 0), region.get("y", 0), region.get("w", 0), region.get("h", 0)

            # Emotion
            emotion = res.get("dominant_emotion", "N/A")

            # Age
            age = res.get("age", "?")

            # Gender (handle possible dict format)
            gender_raw = res.get("gender", "?")
            if isinstance(gender_raw, dict):
                gender = max(gender_raw, key=gender_raw.get)
                confidence = gender_raw[gender]
                gender = f"{gender} ({confidence*100:.1f}%)"
            else:
                gender = gender_raw

            # Multi-line label
            label_lines = [
                f"Emotion: {emotion}",
                f"Gender: {gender}",
                f"Age: {age}"
            ]

            # Draw bounding box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Draw label lines
            for i, line in enumerate(label_lines):
                y_pos = y - 10 - (i * 18)
                cv2.putText(frame, line, (x, y_pos), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 255, 0), 2)

    except Exception as e:
        print("Detection error:", e)

    cv2.imshow("👥 Multi-Person Emotion Detector", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
