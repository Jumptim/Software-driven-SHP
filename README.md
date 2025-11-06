# 🧠 Software‑driven‑SHP: Face Recognition and Hand Gesture Detection

This project performs **real‑time face recognition** and **hand gesture detection**
and sends a **UDP signal (0 or 1)** to MATLAB/Simulink.
The system supports both macOS and Windows platforms via Docker.

---

## 🚀 Features
- Real‑time face recognition using YOLO models
- Hand gesture (“finger‑up”) detection
- UDP output to MATLAB/Simulink (port 5005, uint8)
- Dynamic whitelist management (add/remove faces)
- Camera‑based or image‑based registration
- Unified shell scripts for building and running Docker containers

---

## 📁 Project Structure

---

## 🐳 Docker Setup
### Option 1 – Build from source
```bash
docker build -t face-recognition-infer -f docker/Dockerfile .
docker load -i face-recognition-infer.tar
docker images
docker load -i face-recognition-infer.tar
# Start recognition service
bash scripts/run_recog.sh

# Run local camera recognition
bash scripts/start_camera.sh

# Add new person via camera
bash scripts/run_add.sh
bash scripts/start_camera_add.sh

# Manage whitelist
bash scripts/run_manage.sh
docker system prune -f
zip -r face_project_backup.zip app docker scripts docs

---
