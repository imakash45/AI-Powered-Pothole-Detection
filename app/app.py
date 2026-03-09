# ======================================================
# AI-Powered Pothole Detection System
# Stable Version for College Demo
# ======================================================

import streamlit as st
import cv2
import numpy as np
import tempfile
import time
import platform
from ultralytics import YOLO

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Pothole Detection", layout="wide")

st.title("🚧 AI-Powered Pothole Detection System")

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model():
    return YOLO("best.pt")

model = load_model()

# ---------------- SIDEBAR ----------------
st.sidebar.header("Settings")

confidence = st.sidebar.slider(
    "Confidence Threshold",
    0.1, 1.0, 0.5
)

source = st.sidebar.radio(
    "Select Input Source",
    ["Image", "Video", "Webcam"]
)

# ---------------- GLOBAL VARIABLES ----------------
if "run_webcam" not in st.session_state:
    st.session_state.run_webcam = False

last_beep_time = 0

# ---------------- BEEP FUNCTION (2 sec cooldown) ----------------
def beep():
    global last_beep_time
    now = time.time()
    if now - last_beep_time > 2:
        if platform.system() == "Windows":
            import winsound
            winsound.Beep(1000, 300)
        last_beep_time = now

# ======================================================
# IMAGE DETECTION
# ======================================================
if source == "Image":

    uploaded = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

    if uploaded:
        file_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, 1)

        start = time.time()
        results = model.predict(image, conf=confidence)
        end = time.time()

        annotated = results[0].plot()
        boxes = results[0].boxes
        count = len(boxes)

        col1, col2 = st.columns([3,1])

        with col1:
            st.image(annotated, channels="BGR")

        with col2:
            st.subheader("Detection Info")
            if count > 0:
                st.success(f"Potholes Detected: {count}")
                beep()
            else:
                st.error("No Pothole Detected")

            fps = 1 / (end - start)
            st.info(f"FPS: {fps:.2f}")

# ======================================================
# VIDEO DETECTION
# ======================================================
elif source == "Video":

    uploaded_video = st.file_uploader("Upload Video", type=["mp4", "avi", "mov"])

    if uploaded_video:

        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_video.read())

        cap = cv2.VideoCapture(tfile.name)

        stop = st.button("Stop Video")

        frame_placeholder = st.empty()
        info_placeholder = st.empty()

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret or stop:
                break

            start = time.time()
            results = model.predict(frame, conf=confidence)
            end = time.time()

            annotated = results[0].plot()
            count = len(results[0].boxes)

            frame_placeholder.image(annotated, channels="BGR")

            if count > 0:
                info_placeholder.success(f"Potholes Detected: {count}")
                beep()
            else:
                info_placeholder.warning("No Pothole")

            fps = 1 / (end - start)
            st.sidebar.write(f"FPS: {fps:.2f}")

        cap.release()

# ======================================================
# WEBCAM DETECTION (FIXED PROPERLY)
# ======================================================
elif source == "Webcam":

    col1, col2 = st.columns(2)

    if col1.button("Start Webcam"):
        st.session_state.run_webcam = True

    if col2.button("Stop Webcam"):
        st.session_state.run_webcam = False

    frame_placeholder = st.empty()
    info_placeholder = st.empty()

    if st.session_state.run_webcam:

        cap = cv2.VideoCapture(0)

        while st.session_state.run_webcam:
            ret, frame = cap.read()
            if not ret:
                break

            start = time.time()
            results = model.predict(frame, conf=confidence)
            end = time.time()

            annotated = results[0].plot()
            count = len(results[0].boxes)

            frame_placeholder.image(annotated, channels="BGR")

            if count > 0:
                info_placeholder.success(f"Potholes Detected: {count}")
                beep()
            else:
                info_placeholder.warning("No Pothole")

            fps = 1 / (end - start)
            st.sidebar.write(f"FPS: {fps:.2f}")

        cap.release()