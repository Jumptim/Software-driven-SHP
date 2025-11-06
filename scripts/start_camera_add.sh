#!/bin/bash
#  start_camera_add.sh : quick launch for local whitelist registration

cd "$(dirname "$0")"/../app
python ../host_client/camera_gateway_addwhitelist.py