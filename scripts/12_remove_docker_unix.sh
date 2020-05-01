# Description: Script for removing docker and related images

#!/bin/bash

# Script to remove docker and related images
# 1. make script executable for user $chmod +x 12_remove_docker_unix.sh
# 2. execute script $./12_remove_docker_unix.sh

echo -n password | sudo -S rm -Rf /Applications/Docker
sudo rm -f /usr/local/bin/docker
sudo rm -f /usr/local/bin/docker-machine
sudo rm -f /usr/local/bin/docker-compose
sudo rm -f /usr/local/bin/docker-credential-osxkeychain
sudo rm -Rf ~/.docker
sudo rm -Rf $HOME/Library/Containers/com.docker.docker  # here we delete stored images