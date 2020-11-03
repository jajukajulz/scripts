#!/bin/bash

#How to speed up mouse tracking on a Mac
#$ chmod a+x 17_mac_mouse_scaling.sh
#$ ./17_mac_mouse_scaling.sh

#read current scaling speed (deafult is 3)
defaults read -g com.apple.mouse.scaling

#set speed to 7
defaults write -g com.apple.mouse.scaling 7
