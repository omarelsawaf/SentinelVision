# 🔍 Real-Time Face Recognition & Security Alert System

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org/)
[![DeepFace](https://img.shields.io/badge/DeepFace-Framework-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://github.com/serengil/deepface)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-00FFFF?style=for-the-badge&logoColor=black)](https://ultralytics.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

<p align="center">
  <b>A production-ready, real-time AI computer vision system for face recognition, presence detection, and automated instant Gmail security notifications.</b>
</p>

</div>

---

## 📖 Overview | نظرة عامة

**Face Recognition & Security Alert System** is an intelligent computer vision solution engineered for real-time monitoring and automated alert dispatch. Utilizing state-of-the-art deep learning models (`FaceNet` and `RetinaFace`) through the `DeepFace` framework and `OpenCV`, the system matches incoming camera frames against authorized face embeddings and immediately triggers instant email alerts when authorized or unauthorized personnel are identified.

نظام مراقبة ذكي متكامل يعتمد على تقنيات الرؤية الحاسوبية والذكاء الاصطناعي للتعرف على الوجوه في الوقت الفعلي عبر الكاميرا (أو DroidCam) وإرسال إشعارات وتنبيهات أمنية فورية على البريد الإلكتروني (Gmail) عند رصد أو مطابقة الوجوه المحددة.

---

## ✨ Key Features | المميزات الرئيسية

- 🎯 **State-of-the-Art Recognition**: Utilizes `FaceNet` embeddings and `RetinaFace` detection backend for high-accuracy face verification.
- ⚡ **Optimized Real-Time Performance**: Pre-computes reference face embeddings at startup, running cosine distance checks every $N$ frames to maximize FPS and CPU/GPU efficiency.
- 📧 **Automated Gmail Security Alerts**: Sends formatted HTML/Text security notifications via Gmail SMTP upon face recognition.
- ⏱️ **Smart Cooldown Throttling**: Built-in configurable cooldown interval (e.g. 5 minutes) prevents repetitive alert spamming.
- 🔒 **Secure Configuration**: Complete isolation of sensitive credentials (API keys, App Passwords) using `.env` environment variables.
- 📹 **Flexible Video Inputs**: Supports default USB/laptop webcams, IP cameras, RTSP streams, and mobile camera streams (DroidCam).
- 🏷️ **YOLOv8 Dataset Ready**: Includes dataset structure and configuration (`dataset.yaml`) for custom object/face localization training with YOLOv8.

---

## 🏗️ System Architecture | بنية النظام

```
                +-------------------------+
                |      Camera Stream      | (Webcam / RTSP / DroidCam)
                +------------+------------+
                             |
                             v
                +-------------------------+
                |  Frame Capture (OpenCV) |
                +------------+------------+
                             |  (Every N frames)
                             v
                +-------------------------+
                | Face Detection Backend  | (RetinaFace / OpenCV)
                +------------+------------+
                             |
                             v
                +-------------------------+
                |  Embedding Extraction   | (FaceNet 128/512-d vector)
                +------------+------------+
                             |
                             v
                +-------------------------+
                | Cosine Distance Match   | <--- Reference Embeddings (images/data/)
                +------------+------------+
                             |
                   +---------+---------+
                   |                   |
            [Match < Threshold]   [No Match]
                   |                   |
                   v                   v
      +------------------------+  +------------------------+
      | Display "Match: Name"  |  |   Display "No Match"   |
      | Check Alert Cooldown   |  +------------------------+
      +------------+-----------+
                   | (If cooled down)
                   v
      +------------------------+
      | Send Gmail Security    |
      | Notification via SMTP  |
      +------------------------+
```

---

## 📁 Repository Structure | هيكل المشروع

```
├── images/
│   ├── data/                 # Reference images for authorized individuals (e.g. Omar)
│   └── val/                  # Validation test images
├── locations_dataset/        # YOLO format dataset for face/location detection
│   ├── images/
│   ├── labels/
│   └── dataset.yaml
├── live_face_recognition.py  # 🚀 Main live face recognition & alert script
├── live_face_detection.py    # 👁️ Standalone live face presence detection script
├── my_face_dataset.yaml      # YOLO dataset configuration
├── yolov8n.pt                # YOLOv8 pre-trained weights
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
└── README.md                 # Project documentation
```

---

## 🚀 Quick Start Guide | دليل البدء السريع

### 1. Prerequisites | المتطلبات الأساسية
- **Python 3.10 or 3.11** installed.
- A functional camera (Webcam or DroidCam app connected to the PC).

### 2. Clone the Repository | تحميل المستودع
```bash
git clone https://github.com/omarelsawaf/Face-Recognition-Security-System.git
cd Face-Recognition-Security-System
```

### 3. Create and Activate Virtual Environment | إنشاء البيئة الافتراضية
```bash
# On Windows:
python -m venv venv
.\venv\Scripts\activate

# On Linux / macOS:
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies | تثبيت المكتبات المطلوبة
```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration (.env) | إعداد ملف التكوين

1. Copy the `.env.example` file to create your local `.env`:
   ```bash
   cp .env.example .env
   ```

2. Open `.env` and fill in your settings:
   ```env
   # Gmail Credentials
   SENDER_EMAIL=your_email@gmail.com
   APP_PASSWORD=your_16_character_app_password
   RECEIVER_EMAIL=recipient_email@gmail.com

   # Target Identity
   TARGET_NAME=Omar

   # Recognition Settings
   MODEL_NAME=Facenet
   DETECTOR_BACKEND=retinaface
   DISTANCE_THRESHOLD=0.85

   # Performance & Notification Delay
   CHECK_EVERY_N_FRAMES=10
   COOLDOWN_SECONDS=300

   # Camera Index (0 for primary webcam, or RTSP/DroidCam stream URL)
   CAMERA_SOURCE=0
   ```

> 💡 **How to generate a Gmail App Password:**
> 1. Go to your [Google Account Security Settings](https://myaccount.google.com/security).
> 2. Enable **2-Step Verification** (2FA).
> 3. Search for **App passwords** (كلمات مرور التطبيقات).
> 4. Create a new App Password named e.g. `FaceRecognition` and copy the 16-character generated code into `APP_PASSWORD`.

---

## 🎮 Usage | طريقة التشغيل

### 1. Add Reference Photos
Place 1 or more clear, well-lit photos of the target person in the `images/data/` folder (e.g. `images/data/person1.jpg`).

### 2. Run Face Recognition with Email Alerts
```bash
python live_face_recognition.py
```
- The script computes facial embeddings for reference images at launch.
- The live camera window will display a bounding box indicator:
  - 🟢 **Green ("Match: [Name]")**: Authorized face verified $ightarrow$ Email alert dispatched.
  - 🔴 **Red ("No Match")**: Face detected but does not match authorized embeddings.
  - 🟡 **Yellow ("Scanning / No Face")**: Searching for faces.
- Press **`q`** to safely close the camera stream.

### 3. Run General Face Detection (Without Reference Images)
If you want an alert whenever **any** face appears on camera:
```bash
python live_face_detection.py
```

---

## 📊 Models & Benchmarks

| Model | Detector Backend | Metric | Default Threshold |
|---|---|---|---|
| **FaceNet** (Default) | RetinaFace | Cosine Distance | `0.85` |
| **VGG-Face** | MTCNN / OpenCV | Cosine Distance | `0.68` |
| **ArcFace** | RetinaFace | Cosine Distance | `0.68` |

---

## 🛡️ Security & Privacy

- Sensitive data such as Gmail App Passwords and emails are stored in `.env` and excluded from git tracking via `.gitignore`.
- Reference photos are stored locally on your machine and are not sent to any cloud server.

---

## 👤 Author & Maintainer

- **Developer**: [Omar Elsawaf](https://github.com/omarelsawaf)
- **Email**: omarelsawaf2022@gmail.com
- **GitHub**: [@omarelsawaf](https://github.com/omarelsawaf)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.
