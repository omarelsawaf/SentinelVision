"""
Live Face Detection + Gmail Notification (No Reference Dataset Required)
----------------------------------------------------------------------
This script opens the camera feed and detects if ANY human face appears.
When a face is detected, it sends an instant email notification via Gmail.

Run command:
    python live_face_detection.py

Press 'q' to exit the camera window.
"""

import os
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import cv2
from deepface import DeepFace

# --- Model & Camera Settings ---
CHECK_EVERY_N_FRAMES = 10
DETECTOR_BACKEND = "retinaface"  # Options: retinaface, opencv, ssd, mtcnn

# --- Gmail Notification Settings ---
SENDER_EMAIL = "YOUR_EMAIL@gmail.com"  # Replace with your email address
APP_PASSWORD = "YOUR_APP_PASSWORD"  # Replace with your 16-character App Password
RECEIVER_EMAIL = "RECEIVER_EMAIL@gmail.com"  # Replace with recipient email address

COOLDOWN_SECONDS = (
    300  # Minimum delay between notifications (5 minutes) to prevent spam
)
last_sent_time = 0


def send_gmail_notification():
    """Sends a notification email via Gmail considering cooldown time."""
    global last_sent_time
    current_time = time.time()

    if current_time - last_sent_time < COOLDOWN_SECONDS:
        return

    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL
        msg["Subject"] = "🚨 ALERT: Person Detected on Camera!"

        body = "A face/person was detected on the camera system just now."
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()

        print("\n[NOTIFICATION] ✅ Email notification sent successfully!\n")
        last_sent_time = current_time
    except Exception as e:
        print(f"\n[NOTIFICATION ERROR] ❌ Failed to send notification: {e}\n")


def main():
    print("[INFO] Starting camera feed... Press 'q' to quit.")

    # Open camera stream (0 for built-in webcam or DroidCam IP URL)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] Could not open camera feed.")
        return

    frame_count = 0
    last_label = "Scanning..."
    last_color = (0, 255, 255)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to capture frame from camera.")
            break

        frame_count += 1

        if frame_count % CHECK_EVERY_N_FRAMES == 0:
            try:
                # Extract faces from the current frame
                faces = DeepFace.extract_faces(
                    img_path=frame,
                    detector_backend=DETECTOR_BACKEND,
                    enforce_detection=True,
                )

                if len(faces) > 0:
                    last_label = f"Person Detected ({len(faces)})"
                    last_color = (0, 255, 0)
                    send_gmail_notification()

            except Exception:
                # Exception occurs when no face is found in frame
                last_label = "No Person Detected"
                last_color = (0, 0, 255)

        cv2.putText(
            frame,
            last_label,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            last_color,
            2,
        )

        cv2.imshow("Live Face Detection - press 'q' to quit", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
