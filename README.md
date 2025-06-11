# 🎧 AuraBeat – Emotion-Based Music Playback System

AuraBeat is a real-time facial expression recognition system that detects user emotions via webcam and automatically plays music that matches the mood. Designed for responsive, offline-capable environments such as cars or embedded systems, AuraBeat integrates lightweight AI models, a browser-based interface, and offline playlist caching.

---

## 🚀 Features

- 🎥 **Webcam-based Emotion Detection** using FER models
- 🎵 **Emotion-to-Music Mapping** (Valence–Arousal space)
- 📱 **ReactJS Frontend** for intuitive interaction
- ⚡ **Fast Inference** via TinyCNN and DeepFace (OpenCV/RetinaFace)
- 💾 **Offline Caching** of detected emotions and liked tracks
- 📊 **Admin Panel** to view statistics, emotion trends, and feedback
- 🔐 **Privacy-friendly** – works without login or cloud sync

---

## 🧠 Emotion Recognition Models

| Model                  | Accuracy (%) | FPS (CPU) | Status       |
|------------------------|--------------|-----------|--------------|
| TinyCNN (Custom)       | 54.29        | 11.35     | ✅ Integrated |
| DeepFace (OpenCV)      | 50.00        | 10.62     | ✅ Integrated |
| DeepFace (RetinaFace)  | 42.86        | 0.30      | ✅ Integrated |
| RMN (Simulated)        | 74.10        | 4.70      | 🔄 Planned    |
| ViT-lite (Simulated)   | 71.20        | 1.50      | 🔄 Planned    |

---

## 🧩 System Architecture

```plaintext
```
[ Webcam ] 
    ↓
[ Emotion Detection Backend (Flask + TinyCNN) ]
    ↓
[ Emotion → Music Mapper ]
    ↓
[ Frontend Player UI (React) ]
    ↓
[ Audio Playback + User Feedback Storage ]
📸 UI Preview

```
```
## 🛠️ How to Run
1. Clone Repository
bash
Copy
git clone https://github.com/yourusername/AuraBeat.git
cd AuraBeat
2. Backend (Python + Flask)
bash
Copy
cd backend
pip install -r requirements.txt
python app.py
3. Frontend (React)
bash
Copy
cd frontend
npm install
npm start
📁 Folder Structure
css
Copy
AuraBeat/
├── backend/             ← Flask-based emotion detection
│   ├── models/          ← TinyCNN & DeepFace models
│   └── app.py
├── frontend/            ← ReactJS UI
│   └── src/
├── benchmark/           ← Accuracy and FPS logs
├── figures/             ← Graphs, screenshots, charts
└── README.md
🧪 Datasets Used
FER2013 for model training/evaluation

Internal test images for inference benchmarks

📈 Future Work
Deploy RMN and ViT-lite with GPU acceleration

ONNX.js integration for full browser-side inference

Raspberry Pi deployment with picamera2 and local audio output

Cloud sync for emotion logs and personalized playlists

📜 License
MIT License – see LICENSE file.

👥 Authors
  MA Tiruye

Special thanks to Prof. Foglia and Prof. Prete

```
