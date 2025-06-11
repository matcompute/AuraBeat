# ml_models/utils/hsemotion_loader.py

import cv2
import numpy as np
import onnxruntime as ort

# From AffectNet paper: 7 classes (no valence/arousal for this ONNX)
EMOTION_LABELS = [
    "neutral", "happiness", "surprise", "sadness", "anger", "disgust", "fear"
]

class HSEmotionONNX:
    def __init__(self, model_path):
        self.session = ort.InferenceSession(model_path)
        self.input_name = self.session.get_inputs()[0].name

    def preprocess(self, img):
        # Resize and prepare to [1, 3, 260, 260]
        resized = cv2.resize(img, (260, 260))
        rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        normed = rgb.astype(np.float32) / 255.0
        transposed = np.transpose(normed, (2, 0, 1))  # [H, W, C] -> [C, H, W]
        return np.expand_dims(transposed, axis=0)  # Add batch dim

    def predict(self, img):
        input_blob = self.preprocess(img)
        outputs = self.session.run(None, {self.input_name: input_blob})
        emotion_idx = int(np.argmax(outputs[0]))
        return EMOTION_LABELS[emotion_idx]
