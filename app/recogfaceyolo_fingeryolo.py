import os, time, numpy as np, cv2, torch, platform
from ultralytics import YOLO
import insightface

# ============== PATH CONFIGURATION ==============
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")
DATA_DIR = os.path.join(BASE_DIR, "whitelist_data")

YOLO_FACE_WEIGHTS = os.path.join(MODEL_DIR, "yolov8n-face.pt")
YOLO_GESTURE_WEIGHTS = os.path.join(MODEL_DIR, "yolov8n-gesture.pt")
ENCODINGS_FILE = os.path.join(DATA_DIR, "whitelist_encodings.npy")
NAMES_FILE = os.path.join(DATA_DIR, "whitelist_names.npy")

# ============== PARAMETERS ==============
MATCH_THRESHOLD = 0.55
CONF_THRESHOLD = 0.5
TARGET_GESTURE = "one"

# ============== UTILITIES ==============
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def select_device():
    sys = platform.system().lower()
    if torch.cuda.is_available():
        return "cuda"
    elif sys == "darwin" and torch.backends.mps.is_available():
        return "mps"
    else:
        return "cpu"

# ============== MODEL INITIALIZATION ==============
device = select_device()
print(f"Loading models on device: {device}")

yolo_face = YOLO(YOLO_FACE_WEIGHTS).to(device)
yolo_gesture = YOLO(YOLO_GESTURE_WEIGHTS).to(device)

try:
    app = insightface.app.FaceAnalysis(allowed_modules=['detection','recognition'])
    app.prepare(ctx_id=0)
    print("InsightFace GPU mode loaded")
except Exception as e:
    print(f"GPU init failed, fallback to CPU: {e}")
    app = insightface.app.FaceAnalysis(allowed_modules=['detection','recognition'])
    app.prepare(ctx_id=-1)
    print("InsightFace CPU mode loaded")

def load_whitelist():
    if os.path.exists(ENCODINGS_FILE) and os.path.exists(NAMES_FILE):
        return np.load(ENCODINGS_FILE), np.load(NAMES_FILE)
    return np.array([]), np.array([])

# ============== MAIN INFERENCE FUNCTION ==============
def process_frame(frame):
    encodings, names = load_whitelist()
    boxes = []
    finger_up = False
    matched_name = None

    # ---- Face Recognition ----
    faces = app.get(frame)
    if len(faces) > 0 and len(encodings) > 0:
        biggest = max(faces, key=lambda f: (f.bbox[2]-f.bbox[0])*(f.bbox[3]-f.bbox[1]))
        emb = biggest.embedding
        sims = [cosine_similarity(emb, e) for e in encodings]
        i = np.argmax(sims)
        if sims[i] > MATCH_THRESHOLD:
            matched_name = names[i]
            x1, y1, x2, y2 = map(int, biggest.bbox)
            boxes.append([x1, y1, x2, y2, (0, 255, 0)])
        else:
            for f in faces:
                x1, y1, x2, y2 = map(int, f.bbox)
                boxes.append([x1, y1, x2, y2, (0, 0, 255)])

    # ---- Gesture Detection ----
    g_res = yolo_gesture(frame, conf=CONF_THRESHOLD, verbose=False, device=device)
    for b in g_res[0].boxes:
        cls = int(b.cls[0])
        label = yolo_gesture.names[cls]
        x1, y1, x2, y2 = map(int, b.xyxy[0])
        if label.lower() == TARGET_GESTURE:
            color = (0, 255, 0)
            finger_up = True
        else:
            color = (0, 0, 255)
        boxes.append([x1, y1, x2, y2, color])

    text = "Finger Up!" if finger_up else ""
    button = 1 if (matched_name is not None and finger_up) else 0

    return {
        "boxes": boxes,
        "text": text,
        "name": str(matched_name) if matched_name else "",
        "button": button
    }