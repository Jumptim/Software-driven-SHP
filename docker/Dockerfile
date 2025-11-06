# =========================================================
# Base: Python 3.9, multi‑arch (amd64, arm64, Apple M‑series)
# =========================================================
FROM python:3.9-slim

WORKDIR /app

# ----- System dependencies -----
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cmake pkg-config \
    libglib2.0-0 libsm6 libxrender1 libxext6 libgl1 \
 && rm -rf /var/lib/apt/lists/*

# ----- Copy requirements -----
COPY docker/requirements.txt /app/

# ----- Install pip & requirements -----
RUN pip install --no-cache-dir --upgrade "pip<24.1"
RUN pip install --no-cache-dir -r /app/requirements.txt

# ----- Fix NumPy build (force reinstall from source) -----
RUN pip install --no-cache-dir --upgrade --force-reinstall numpy

# ----- Install PyTorch (auto CPU/GPU build) -----
RUN pip install --no-cache-dir \
    torch==2.0.1+cu118 \
    torchvision==0.15.2+cu118 \
    torchaudio==2.0.2+cu118 \
    -f https://download.pytorch.org/whl/torch_stable.html || \
    pip install --no-cache-dir torch torchvision torchaudio

# ----- Copy full application -----
COPY ../app /app
COPY docker/entrypoint.sh /app/

RUN chmod +x /app/entrypoint.sh

EXPOSE 9000 9100
ENTRYPOINT ["/app/entrypoint.sh"]