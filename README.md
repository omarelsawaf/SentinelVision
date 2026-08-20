# 🔍 Real-Time Face Recognition & Security Alert System

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org/)
[![DeepFace](https://img.shields.io/badge/DeepFace-Framework-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://github.com/serengil/deepface)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

<p align="center">
  <b>A real-time AI computer vision system framework for face recognition and automated instant security notifications.</b>
</p>

</div>

---

## 📖 Overview | نظرة عامة

**Face Recognition & Security Alert System** is an intelligent computer vision solution designed for real-time monitoring and automated email alert dispatch using DeepFace and OpenCV.

نظام مراقبة ذكي يعتمد على تقنيات الرؤية الحاسوبية والذكاء الاصطناعي للتعرف على الوجوه في الوقت الفعلي وإرسال إشعارات وتنبيهات أمنية فورية على البريد الإلكتروني (Gmail).

---

## 📁 Repository Structure | هيكل المشروع

```
├── images/
│   └── data/                 # Reference images directory
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

### 3. Install Dependencies | تثبيت المكتبات المطلوبة
```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration (.env) | إعداد ملف التكوين

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Configure your Gmail credentials and camera settings inside `.env`.

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
