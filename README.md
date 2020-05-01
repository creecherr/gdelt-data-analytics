
# Overview

This Data Analytics Service queries of GDELT Data using Google Big Query, transforms this data, and adds it to a Firebase Database.
This application also returns a dynamic report of this data. For information about the actual API endpoints please view the openapi_spec.yaml file.

## What is GDELT? 
This project monitors the world's broadcast, print, and web news from nearly every corner of every country in over 100 languages and identifies the people, locations, organizations, counts, themes, sources, emotions, quotes, images and events driving our global society every second of every day.

# How to run this project

## Prerequisites

- Install docker

# How to Run
1. Clone the repo from the following link (insert link here)
2. Install python 3.7 and docker on your local machine.
3. In order to run this service on your local docker you will need docker swarm. Run docker swarm init command.
4. This service is using docker secrets so you will be needing all the secrets to be added to your docker service.
5. After cloning the service cd into the repo directory from terminal and run "docker build -t your_image_name ."
6. Steps to add docker secrets:
   - We need all secrets to be added to local docker service 
   
   - Command to create secret:
       
      printf "the right url" | docker secret create base_url -
       or files: (make sure you are in right folder where ever you have your certs)
       
       docker secret create cert ./cert
7. docker service create --secret base_url(mention all the secrets that you have created by adding a space --secret your_secret)  --name your_service_name -p 8080:8080 your_image
8. check the logs by following docker service logs your_service_name --follow
