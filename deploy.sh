#!/bin/bash

echo "Deploying to the production environment"

echo "Removing old containers"
sudo docker rm -f compose_nginx_1 &&
sudo docker rm -f compose_web_1 &&
sudo docker rm -f compose_celery_1 &&
sudo docker rm -f compose_redis_1 &&
sudo docker rm -f compose_flower_1 &&

echo "Building new containers and starting them"
sudo docker-compose -f ./compose/docker-compose.prod.yml up -d --build &&
echo "Done"