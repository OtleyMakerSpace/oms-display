#!/bin/bash

# disable screen saver timeout
xset -display :0 s 0 0

# disable blanking timeout
xset -display :0 dpms 0 0 0

cd /home/pi/oms-display
git pull >git.log 2>&1
source .venv/bin/activate
pip install -r requirements.txt
python OMS_slide_show.py
