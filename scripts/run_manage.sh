#!/bin/bash
#  run_manage.sh : start Docker whitelist manager (view/delete/import)

docker run -it --rm \
  -v $(pwd)/app/whitelist_data:/app/whitelist_data \
  -v $(pwd)/app/whitelist_images:/app/whitelist_images \
  face-recognition-infer manage