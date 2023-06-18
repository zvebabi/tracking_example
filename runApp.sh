#!/bin/bash 
set -euo pipefail

if [ $# -eq 0 ]
  then
    echo "Usage: $0 tracking_history (length of the object path in pixels)"
    exit
fi

track_history=$1

if [ -f /.dockerenv ]; then
#   gdown -O /FairMOT/models/fairmot_dla34.pth \
    #   --fuzzy https://drive.google.com/open?id=1iqRQjsG9BawIl8SlFomMg5iwkb6nqSpi&authuser=0
  python3 tracking_demo.py mot --input-video ./HallWayTracking/videos/001.avi \
    --output-root /demos \
    --track_history $track_history \
    --topview_path /app/images/floor_plan.png \
    --input_h 480 --input_w 640 \
    --load_model ./FairMOT/models/fairmot_dla34.pth \
    --conf_thres 0.5
else
  echo "This script should be run inside a container"
fi