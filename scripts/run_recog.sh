#!/bin/bash
#  run_recog.sh : start Docker real-time recognition service

docker run -it --rm \
  -p 9000:9000 \
  -v $(pwd)/app/whitelist_data:/app/whitelist_data \
  -v $(pwd)/app/whitelist_images:/app/whitelist_images \
  face-recognition-infer recog