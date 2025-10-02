#!/bin/bash

mkdir -p SAVED_FRAMES

sudo docker network create --subnet=172.18.0.0/24 external
sudo docker-compose down
sudo docker-compose up -d --build
