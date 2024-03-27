#!/bin/bash

# Switch to superuser
sudo su

# Update packages and install necessary software
apt update
apt install -y apt-transport-https ca-certificates curl software-properties-common

# Set up Docker repository and install Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
apt-cache policy docker-ce
apt install -y docker-ce

# Install Docker Compose, Make, and Nginx
apt install -y docker-compose
apt install -y make
apt install -y nginx

# Clone your GitHub repository
cd /var/www
git clone https://github.com/oridosai/img2txt-fine-tuning-api.git
