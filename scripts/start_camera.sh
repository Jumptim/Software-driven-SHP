#!/bin/bash
#  start_camera.sh : quick launch of local recognition interface

cd "$(dirname "$0")"/../app
python ../host_client/camera_gateway.py