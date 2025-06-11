# rmn_model.py

import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image
import cv2
import time

class RMNEmotionModel(nn.Module):
    def __init__(self):
        super(RMNEmotionModel, self).__init__()
        self.model = torch.hub.load('deepinsight/insightface', 'rmn', source='github', pretrained=True)
        self.model.eval()

    def predict(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        transform = transforms.Compose([
            transforms.Resize((112, 112)),
            transforms.ToTensor(),
        ])
        img = transform(img).unsqueeze(0)
        with torch.no_grad():
            output = self.model(img)
            pred = torch.argmax(output, dim=1).item()
        return pred

def evaluate_rmn(images, class_labels):
    model = RMNEmotionModel()
    correct = 0
    total = 0
    start = time.time()
    for img, label in images:
        try:
            pred_idx = model.predict(img)
            pred_label = class_labels[pred_idx]
            if pred_label.lower() == label.lower():
                correct += 1
        except Exception as e:
            print("RMN error:", e)
        total += 1
    end = time.time()
    return {
        "model": "RMN",
        "accuracy": round(correct / total * 100, 2),
        "fps": round(total / (end - start), 2)
    }
