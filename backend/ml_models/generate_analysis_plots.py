import os
import json
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report

# === CONFIG ===
RESULT_DIR = "ml_models/results"
os.makedirs(RESULT_DIR, exist_ok=True)

LABELS = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

# === TRUE vs PREDICTED (Update this if you want more samples)
y_true = ['happy', 'sad', 'angry', 'happy', 'neutral', 'surprise', 'sad', 'happy', 'neutral', 'angry']
y_pred = ['happy', 'sad', 'neutral', 'happy', 'neutral', 'surprise', 'angry', 'happy', 'happy', 'angry']

# === CONFUSION MATRIX ===
def plot_confusion_matrix(y_true, y_pred, labels):
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=labels, yticklabels=labels)
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    path = os.path.join(RESULT_DIR, "confusion_matrix_final.png")
    plt.savefig(path)
    plt.close()
    print(f"[✅] Saved: {path}")

# === RADAR CHART ===
def plot_radar(y_true, y_pred, labels):
    accuracy_per_class = []
    for label in labels:
        tp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == label and yp == label)
        total = sum(1 for yt in y_true if yt == label)
        acc = tp / total if total else 0
        accuracy_per_class.append(acc * 100)

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    accuracy_per_class += accuracy_per_class[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, accuracy_per_class, "o-", linewidth=2, color="orange")
    ax.fill(angles, accuracy_per_class, alpha=0.25, color="orange")
    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    ax.set_title("Emotion-wise Accuracy (%)")
    ax.grid(True)
    plt.tight_layout()
    path = os.path.join(RESULT_DIR, "emotion_radar_final.png")
    plt.savefig(path)
    plt.close()
    print(f"[✅] Saved: {path}")

# === CLASSIFICATION REPORT ===
def save_classification_report(y_true, y_pred, labels):
    report = classification_report(
        y_true, y_pred, labels=labels, output_dict=True, zero_division=0
    )
    path = os.path.join(RESULT_DIR, "classification_report_final.json")
    with open(path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"[✅] Saved: {path}")

# === BENCHMARK COMPARISON CHARTS ===
def plot_benchmark_charts():
    benchmark_results = [
        {"model": "TinyCNN", "accuracy": 54.29, "fps": 10.4},
        {"model": "DeepFace-retinaface", "accuracy": 42.86, "fps": 0.3},
        {"model": "DeepFace-opencv", "accuracy": 50.0, "fps": 5.19}
    ]
    path_json = os.path.join(RESULT_DIR, "benchmark_final.json")
    with open(path_json, "w") as f:
        json.dump(benchmark_results, f, indent=2)
    print(f"[✅] Saved: {path_json}")

    df = pd.DataFrame(benchmark_results)

    # Accuracy bar chart
    plt.figure(figsize=(6, 4))
    plt.bar(df["model"], df["accuracy"], color='skyblue')
    plt.ylabel("Accuracy (%)")
    plt.title("Model Accuracy Comparison")
    plt.ylim(0, 100)
    plt.tight_layout()
    path_acc = os.path.join(RESULT_DIR, "model_accuracy_comparison_final.png")
    plt.savefig(path_acc)
    plt.close()
    print(f"[✅] Saved: {path_acc}")

    # FPS bar chart
    plt.figure(figsize=(6, 4))
    plt.bar(df["model"], df["fps"], color='lightgreen')
    plt.ylabel("Frames Per Second (FPS)")
    plt.title("Model Inference Speed")
    plt.tight_layout()
    path_fps = os.path.join(RESULT_DIR, "model_fps_comparison_final.png")
    plt.savefig(path_fps)
    plt.close()
    print(f"[✅] Saved: {path_fps}")

# === RUN ALL ===
plot_confusion_matrix(y_true, y_pred, LABELS)
plot_radar(y_true, y_pred, LABELS)
save_classification_report(y_true, y_pred, LABELS)
plot_benchmark_charts()
