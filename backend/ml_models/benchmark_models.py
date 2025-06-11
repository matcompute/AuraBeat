import os
import json
import time
import cv2
import numpy as np
from deepface import DeepFace
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from utils.rmn_model import evaluate_rmn
from utils.vit_emotion import evaluate_vit  # <-- NEW import

# === CONFIG ===
test_image_dir = "../ml_models/datasets/test"
tinycnn_path = "../ml_models/models/tiny_cnn.h5"
output_path = "../ml_models/results/benchmark_full.json"
img_size_tinycnn = 48
class_labels = sorted(os.listdir(test_image_dir))

# === LOAD TEST IMAGES ===
def get_test_images(n_per_class=10):
    images = []
    for label in class_labels:
        folder = os.path.join(test_image_dir, label)
        files = os.listdir(folder)[:n_per_class]
        for file in files:
            path = os.path.join(folder, file)
            img = cv2.imread(path)
            if img is None:
                continue
            images.append((img, label))
    return images

# === EVALUATE TINYCNN ===
def evaluate_tinycnn(model, images):
    correct = 0
    start = time.time()
    for img, label in images:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (img_size_tinycnn, img_size_tinycnn))
        normed = resized.astype("float32") / 255.0
        input_img = np.expand_dims(img_to_array(normed), axis=0)
        pred = model.predict(input_img, verbose=0)[0]
        pred_label = class_labels[np.argmax(pred)]
        if pred_label.lower() == label.lower():
            correct += 1
    end = time.time()
    return {
        "model": "TinyCNN",
        "accuracy": round(correct / len(images) * 100, 2),
        "fps": round(len(images) / (end - start), 2)
    }

# === EVALUATE DEEPFACE ===
def evaluate_deepface(images, backend="opencv"):
    correct = 0
    start = time.time()
    for img, label in images:
        resized = cv2.resize(img, (224, 224))
        rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        try:
            result = DeepFace.analyze(rgb, actions=["emotion"], detector_backend=backend, enforce_detection=False)
            if isinstance(result, list): result = result[0]
            pred_label = result.get("dominant_emotion", "").lower()
            if pred_label == label.lower():
                correct += 1
        except Exception as e:
            print(f"[DeepFace-{backend}] Error:", e)
    end = time.time()
    return {
        "model": f"DeepFace-{backend}",
        "accuracy": round(correct / len(images) * 100, 2),
        "fps": round(len(images) / (end - start), 2)
    }

# === MAIN ===
def main():
    print("🔍 Loading test images...")
    images = get_test_images(n_per_class=10)
    results = []

    print("🚀 Evaluating TinyCNN...")
    tinycnn = load_model(tinycnn_path)
    results.append(evaluate_tinycnn(tinycnn, images))

    print("🚀 Evaluating DeepFace (VGG)...")
    results.append(evaluate_deepface(images, backend="retinaface"))

    print("🚀 Evaluating DeepFace (OpenCV)...")
    results.append(evaluate_deepface(images, backend="opencv"))

    print("🚀 Evaluating RMN...")
    results.append(evaluate_rmn(images, class_labels))

    print("🚀 Evaluating ViT (mock)...")
    results.append(evaluate_vit(images, class_labels))

    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"✅ Results saved to: {output_path}")
    for r in results:
        print(f"{r['model']:20} | Accuracy: {r['accuracy']}% | FPS: {r['fps']}")

if __name__ == "__main__":
    main()
