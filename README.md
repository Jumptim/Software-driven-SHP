cd ~/Software-driven-SHP

cat > README.md << 'EOF'
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
- Unified shell scripts for building and running containers  

---

## 📁 Project Structure

Software-driven-SHP/

├── app/                      → Main application logic  
│   ├── models/               → Model weights (YOLO face / gesture)  
│   ├── whitelist_data/       → Encodings and authorized names  
│   └── whitelist_images/     → Reference images for whitelist  
├── docker/                   → Dockerfile and dependencies  
├── scripts/                  → Bash scripts (build/run/manage)  
├── host_client/              → Windows client programs  
├── docs/                     → Manuals (Mac + Windows)  
├── Detailed_Simulation_recogface_finger_yolo.slx → Simulink test  
└── README.md  

---

## 🐳 Docker Setup

Option 1 – Build from source:
    docker build -t face-recognition-infer -f docker/Dockerfile .

Option 2 – Load prebuilt image:
    docker load -i face-recognition-infer.tar
    docker images

---

## 📦 Prebuilt Docker Image
Download the prebuilt image from [GitHub Releases](https://github.com/Jumptim/Software-driven-SHP/releases):

    docker load -i face-recognition-infer.tar

---

## ▶️ Running the Application

    bash scripts/run_recog.sh        # Run recognition service  
    bash scripts/start_camera.sh     # Start camera client  
    bash scripts/run_add.sh          # Add new person service  
    bash scripts/start_camera_add.sh # Add with camera  
    bash scripts/run_manage.sh       # Manage whitelist  

---

## 🧩 MATLAB / Simulink Integration (optional)

UDP Receive Block:
| Parameter | Value |
|------------|-------|
| Port | 5005 |
| Data type | uint8 |
| Size | 1 |

Behavior:
- Face recognized + Gesture up → 1  
- Otherwise → 0  

---

## 🧼 Cleanup and Backup

    docker system prune -f
    zip -r face_project_backup.zip app docker scripts docs

---

## 👨‍💻 Authors
Maintainer: Jumptim  
Contributor: wzy (Zywang1234)  
Platform: macOS 12+ / Windows 10+ / Docker 24+  

---

## 📜 License
This repository is for academic and research use only.  
Please cite appropriately in derived works.  
EOF