#!/bin/sh
# entrypoint.sh: choose which service to start in container

set -eu
echo "🟢 Entrypoint started with args: $@"

MODE="${1:-}"

case "$MODE" in
  recog)
    echo "🚀 Starting real-time inference server (port 9000)..."
    shift
    exec python /app/inference_server.py "$@"
    ;;
  add)
    echo "🧠 Starting whitelist-add server (port 9100)..."
    shift
    exec python /app/inference_server_addwhitelist.py "$@"
    ;;
  manage)
    echo "🧾 Opening whitelist manager ..."
    shift
    exec python /app/manage_whitelist.py "$@"
    ;;
  *)
    echo "Usage:"
    echo "  docker run -it face-recognition-infer recog"
    echo "  docker run -it face-recognition-infer add"
    echo "  docker run -it face-recognition-infer manage"
    exit 1
    ;;
esac