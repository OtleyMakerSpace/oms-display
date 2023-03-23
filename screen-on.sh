#!/bin/bash

tvservice -p
sleep 0.5
xset -display :0 dpms force on
xset -display :0 -dpms
