#!/bin/bash

source ~/.virtualenvs/fresh/bin/activate

while true
do      
    python3 ~/code/gactions-computer-controller/apps/video_player/listener/listener.py
    sleep 2
done
