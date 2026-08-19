"""
Live Face Detection & Alert System (General Detection)
------------------------------------------------------
Detects any human face in the camera stream and dispatches
an instant security email alert without requiring reference images.

Usage:
    python live_face_detection.py

Press 'q' to exit.
"""

import os
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import cv2
from deepface import DeepFace
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- Settings ---
CHECK_EVERY_N_FRAMES = int(os.getenv("CHECK_EVERY_N_FRAMES", "10"))
DETECTOR_BACKEND = os.getenv("DETECTOR_BACKEND", "retinaface")
CAMERA_SOURCE = os.getenv("CAMERA_SOURCE", "0")
try:
    CAMERA_SOURCE = int(CAMERA_SOURCE)
except ValueError:
    pass

SENDER_EMAIL = os.getenv("SENDER_EMAIL", "")
APP_PASSWORD = os.getenv("APP_PASSWORD", "")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL", "")
COOLDOWN_SECONDS = int(os.getenv("COOLDOWN_SECONDS", "300"))

last_sent_time = 0


def send_gmail_notification(face_count: int = 1):
    """Sends a notification email via Gmail with cooldown protection."""
    global last_sent_time
    current_time = time.time()

    if current_time - last_sent_time < COOLDOWN_SECONDS:
        return

    if not SENDER_EMAIL or not APP_PASSWORD or not RECEIVER_EMAIL:
        print("[WARN] Gmail credentials not configured in .env. Skipping notification.")
        return

    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL
        msg["Subject"] = "🚨 تنبيه أمني: تم رصد وجود أشخاص أمام الكاميرا!"

        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        body = (
            f"تم رصد وجه بشري بواسطة نظام المراقبة الذكي.\n"
            f"عدد الوجوه المكتشفة: {face_count}\n"
            f"الوقت: {timestamp}\n"
            f"Detector: {DETECTOR_BACKEND}\n"
        )
        msg.attach(MIMEText(body, "plain", "utf-8"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()

        print(f"\n[NOTIFICATION] ✅ تم إرسال إشعار الرصد إلى ({RECEIVER_EMAIL}) بنجاح!\n")
        last_sent_time = current_time
    except Exception as e:
        print(f"\n[NOTIFICATION ERROR] ❌ فشل إرسال الإشعار: {e}\n")


def main():
    print("=" * 60)
    print("  👁️ Live Face Detection & Security Alert System")
    print("=" * 60)
    print(f"[INFO] جاري فتح الكاميرا ({CAMERA_SOURCE})... اضغط 'q' للخروج.")

    cap = cv2.VideoCapture(CAMERA_SOURCE)
    if not cap.isOpened():
        print(f"[ERROR] تعذر فتح الكاميرا: {CAMERA_SOURCE}")
        return

    frame_count = 0
    last_label = "Scanning..."
    last_color = (0, 255, 255)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] فشل التقاط الفريم.")
            break

        frame_count += 1

        if frame_count % CHECK_EVERY_N_FRAMES == 0:
            try:
                faces = DeepFace.extract_faces(
                    img_path=frame,
                    detector_backend=DETECTOR_BACKEND,
                    enforce_detection=True,
                )

                if len(faces) > 0:
                    last_label = f"Person Detected ({len(faces)})"
                    last_color = (0, 255, 0)
                    send_gmail_notification(len(faces))

            except Exception:
                last_label = "No Person Detected"
                last_color = (0, 0, 255)

        cv2.putText(
            frame,
            last_label,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            last_color,
            2,
        )

        cv2.imshow("Live Face Detection - Press 'q' to Quit", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("[INFO] تم إغلاق البرنامج بنجاح.")


if __name__ == "__main__":
    main()
