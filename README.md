# 🛡️ SentinelVision

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org/)
[![DeepFace](https://img.shields.io/badge/DeepFace-Framework-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://github.com/serengil/deepface)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

<p align="center">
  <b>SentinelVision: Real-time AI Face & Presence Detection System with Instant Automated Gmail Security Notifications.</b>
</p>

</div>

---

## 📖 Overview | نظرة عامة

**SentinelVision** is a lightweight, real-time computer vision security system designed to monitor live camera streams (Webcam), detect human presence and faces using deep learning backends (RetinaFace / OpenCV), and dispatch instant email alerts via Gmail SMTP.

نظام مراقبة وتنبيه أمني ذكي يعتمد على الرؤية الحاسوبية والذكاء الاصطناعي لرصد الوجوه وحركة الأشخاص في الوقت الفعلي عبر الكاميرا وإرسال إشعارات وتنبيهات أمنية فورية على الجيميل.

---

## 📦 Libraries & Dependencies | المكتبات المستخدمة

| Library | Type | Purpose |
|---|---|---|
| **`opencv-python`** (`cv2`) | External (`pip install`) | التقاط وتحليل فيديو الكاميرا في الوقت الفعلي |
| **`deepface`** | External (`pip install`) | رصد واكتشاف الوجوه بدقة عبر موديل RetinaFace |
| **`smtplib`** | Built-in (مدمجة مع بايثون) | الاتصال بسيرفر Gmail وإرسال الإشعارات عبر بروتوكول SMTP |
| **`time`** | Built-in (مدمجة مع بايثون) | إدارة الفواصل الزمنية وفترات التهدئة (Cooldown) لمنع تكرار الرسائل |
| **`email`** | Built-in (مدمجة مع بايثون) | تنسيق وبناء رسائل البريد الإلكتروني (MIMEMultipart) |

---

## ✨ Key Features | المميزات

- 👁️ **Live Face & Presence Detection**: Automatically detects any human face appearing in the camera feed.
- 📧 **Instant Gmail Alerts**: Dispatches security notification emails with timestamp and details.
- ⏱️ **Smart Alert Cooldown**: Configurable cooldown threshold (default 5 mins) to avoid spam.
- 📹 **Flexible Camera Feeds**: Works with built-in webcams and external USB cameras.
- 🚀 **Zero Dataset Setup**: Ready to run out of the box without requiring pre-trained reference databases.

---

## 📁 Repository Structure | هيكل المستودع

```
├── SentinelVision.py         # 🚀 Main SentinelVision detection & alert script
├── requirements.txt          # Dependencies (opencv-python, deepface)
├── .env.example              # Configuration template
├── .gitignore                # Git ignore rules
├── LICENSE                   # MIT License
└── README.md                 # Project documentation
```

---

## 🚀 Quick Start | طريقة التشغيل

### 1. Clone & Setup | تحميل المستودع
```bash
git clone https://github.com/omarelsawaf/SentinelVision.git
cd SentinelVision
```

### 2. Install Dependencies | تثبيت المكتبات
```bash
pip install -r requirements.txt
```

### 3. Run SentinelVision | تشغيل البرنامج
```bash
python SentinelVision.py
```
> اضغط **`q`** للخروج وإغلاق نافذة الكاميرا بأمان.

---

## ⚙️ Configuration | إعداد البريد الإلكتروني
افتح ملف `SentinelVision.py` وقم بتعيين بيانات الجيميل:
- `SENDER_EMAIL`: بريدك الإلكتروني الذي سيرسل الإشعار.
- `APP_PASSWORD`: كلمة مرور التطبيقات المكونة من 16 حرفاً (Gmail App Password).
- `RECEIVER_EMAIL`: البريد الإلكتروني الذي سيستقبل التنبيه.

---

## 👤 Author

- **Developer**: [Omar Elsawaf](https://github.com/omarelsawaf)
- **GitHub**: [@omarelsawaf](https://github.com/omarelsawaf)

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
