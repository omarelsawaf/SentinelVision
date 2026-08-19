"""
Live Face Recognition & Security Alert System
---------------------------------------------
Real-time face recognition using DeepFace (FaceNet / RetinaFace) + OpenCV.
Dispatches instant Gmail security alerts upon detecting matched faces.

Usage:
    python live_face_recognition.py

Press 'q' to exit the camera window.
"""

import os
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import cv2
from deepface import DeepFace
from dotenv import load_dotenv
import numpy as np

# Load environment variables from .env file
load_dotenv()

# --- Configuration & Model Settings ---
REFERENCE_DIR = [
    os.path.join("images", "data"),
]

CHECK_EVERY_N_FRAMES = int(os.getenv("CHECK_EVERY_N_FRAMES", "10"))
MODEL_NAME = os.getenv("MODEL_NAME", "Facenet")
DETECTOR_BACKEND = os.getenv("DETECTOR_BACKEND", "retinaface")
DISTANCE_THRESHOLD = float(os.getenv("DISTANCE_THRESHOLD", "0.85"))
CAMERA_SOURCE = os.getenv("CAMERA_SOURCE", "0")
TARGET_NAME = os.getenv("TARGET_NAME", "Omar")

# Parse camera source (int for device index, string for RTSP/DroidCam URL)
try:
    CAMERA_SOURCE = int(CAMERA_SOURCE)
except ValueError:
    pass

# --- Gmail Notification Settings ---
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "")
APP_PASSWORD = os.getenv("APP_PASSWORD", "")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL", "")
COOLDOWN_SECONDS = int(os.getenv("COOLDOWN_SECONDS", "300"))

last_sent_time = 0


def send_gmail_notification(person_name: str = "Authorized User"):
    """Sends an email notification via Gmail with cooldown throttling."""
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
        msg["Subject"] = f"🚨 تنبيه أمني: تم التعرف على ({person_name})!"

        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        body = (
            f"تم الكشف عن مطابقة للوجه في نظام المراقبة.
"
            f"الاسم: {person_name}
"
            f"الوقت: {timestamp}
"
            f"الموديل المستخدم: {MODEL_NAME} ({DETECTOR_BACKEND})
"
        )
        msg.attach(MIMEText(body, "plain", "utf-8"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()

        print(f"\n[NOTIFICATION] ✅ تم إرسال إشعار أمني إلى ({RECEIVER_EMAIL}) بنجاح!\n")
        last_sent_time = current_time
    except Exception as e:
        print(f"\n[NOTIFICATION ERROR] ❌ فشل إرسال الإشعار: {e}\n")


def get_reference_images(folders):
    """Retrieves all valid image paths from the reference folders."""
    valid_ext = (".jpg", ".jpeg", ".png", ".webp")
    images = []
    for folder in folders:
        if not os.path.isdir(folder):
            print(f"[WARN] المجلد غير موجود وسيتم تجاهله: {folder}")
            continue
        images.extend(
            os.path.join(folder, f)
            for f in os.listdir(folder)
            if f.lower().endswith(valid_ext)
        )
    return images


def compute_embeddings(image_paths):
    """Computes facial embeddings for all reference images at startup."""
    embeddings = []
    for path in image_paths:
        try:
            reps = DeepFace.represent(
                img_path=path,
                model_name=MODEL_NAME,
                detector_backend=DETECTOR_BACKEND,
                enforce_detection=True,
            )
            embeddings.append(np.array(reps[0]["embedding"]))
            print(f"[OK] تم استخراج بصمة الوجه من: {path}")
        except Exception as e:
            print(f"[WARN] تعذر استخراج بصمة الوجه من: {path} ({e})")

    return embeddings


def cosine_distance(a, b):
    """Calculates cosine distance between two embedding vectors."""
    dot = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 1.0
    return 1 - (dot / (norm_a * norm_b))


def main():
    print("=" * 60)
    print("  🚀 Live Face Recognition & Security Alert System")
    print("=" * 60)

    reference_paths = get_reference_images(REFERENCE_DIR)
    if not reference_paths:
        print(f"[ERROR] لا توجد صور مرجعية في المجلدات: {REFERENCE_DIR}")
        print("[HINT] أضف صور الوجه في مجلد images/data/")
        return

    print(f"[INFO] تم العثور على {len(reference_paths)} صورة مرجعية.")
    print("[INFO] جاري استخراج البصمات المرجعية...")
    reference_embeddings = compute_embeddings(reference_paths)

    if not reference_embeddings:
        print("[ERROR] لم يتم العثور على أي بصمة وجه صالحة في الصور المرجعية.")
        return

    print(f"[INFO] تم تجهيز {len(reference_embeddings)} بصمة بنجاح.")
    print(f"[INFO] جاري الاتصال بالكاميرا ({CAMERA_SOURCE})... اضغط 'q' للخروج.")

    cap = cv2.VideoCapture(CAMERA_SOURCE)
    if not cap.isOpened():
        print(f"[ERROR] يتعذر فتح الكاميرا: {CAMERA_SOURCE}")
        return

    frame_count = 0
    last_label = "Scanning..."
    last_color = (0, 255, 255)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] تعذر التقاط فريم من الكاميرا.")
            break

        frame_count += 1

        if frame_count % CHECK_EVERY_N_FRAMES == 0:
            try:
                reps = DeepFace.represent(
                    img_path=frame,
                    model_name=MODEL_NAME,
                    detector_backend=DETECTOR_BACKEND,
                    enforce_detection=True,
                )
                current_embedding = np.array(reps[0]["embedding"])

                distances = [
                    cosine_distance(current_embedding, ref_emb)
                    for ref_emb in reference_embeddings
                ]
                best_distance = min(distances)

                if best_distance < DISTANCE_THRESHOLD:
                    last_label = f"Match: {TARGET_NAME} ({best_distance:.2f})"
                    last_color = (0, 255, 0)
                    send_gmail_notification(TARGET_NAME)
                else:
                    last_label = f"No Match ({best_distance:.2f})"
                    last_color = (0, 0, 255)

            except Exception:
                last_label = "No Face Detected"
                last_color = (0, 255, 255)

        cv2.putText(
            frame,
            last_label,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            last_color,
            2,
        )

        cv2.imshow("Live Face Recognition - Press 'q' to Quit", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("[INFO] تم إغلاق البرنامج بنجاح.")


if __name__ == "__main__":
    main()
