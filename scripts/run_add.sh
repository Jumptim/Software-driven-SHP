#!/bin/bash
#  run_add.sh : start Docker whitelist registration service

docker run -it --rm \
  -p 9100:9100 \
  -v $(pwd)/app/whitelist_data:/app/whitelist_data \
  -v $(pwd)/app/whitelist_images:/app/whitelist_images \
  face-recognition-infer add