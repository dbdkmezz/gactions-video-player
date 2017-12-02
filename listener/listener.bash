#!/bin/bash

source ~/.virtualenvs/fresh/bin/activate

while true
do      
    python3 ~/code/gactions-computer-controller/listener/listener.py
    sleep 2
done
