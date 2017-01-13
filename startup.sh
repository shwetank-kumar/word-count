#!/bin/bash
# Check if docker is running
var=$(docker ps -a -f name=rabbit-server --format "{{.Names}}")
if [[ ! -z $var ]]
  then echo "rabbit-server is running"
else
    echo "starting rabbit-server..."
  # Run Rabbitmq server in a docker
  docker run -d --hostname my-rabbit --name rabbit-server \
  -e RABBITMQ_DEFAULT_USER=user \
  -e RABBITMQ_DEFAULT_PASS=password -p 8080:5672 rabbitmq:3-management
fi
