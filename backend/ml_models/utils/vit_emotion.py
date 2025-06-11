# utils/vit_emotion.py

import time
import numpy as np
import cv2
import random

# MOCK class for ViT emotion recognition
def evaluate_vit(images, class_labels):
    print("⚠️ Using MOCK ViT evaluator (just for comparison)...")
    correct = 0
    start = time.time()
    
    for img, label in images:
        pred_label = random.choice(class_labels)  # random guess
        if pred_label.lower() == label.lower():
            correct += 1

    end = time.time()
    return {
        "model": "ViT-Mock",
        "accuracy": round(correct / len(images) * 100, 2),
        "fps": round(len(images) / (end - start), 2)
    }
