#!/bin/bash
# Create network to which all services connect
function create_network()
{
  docker network create redis-celery
}

# Start redis server
function start_redis()
{
  docker run -d -p 6379:6379 --name redis-server --net=redis-celery redis
}

# Stop redis server
function stop_redis()
{
  docker stop redis-server
}

# Delete redis container
function delete_redis_container()
{
  docker rm redis-server
}

# Delete redis image
function delete_redis_image()
{
  docker rmi redis
}

# Build celery image
function build_celery()
{
    docker build -f ./Dockerfile.celery -t celery .
}

# Run celery image
function run_celery()
{
  docker run --name celery-worker --net=redis-celery --rm=false celery
}

# Start celery container
function start_celery()
{
  docker start celery-worker
}

# Stop celery container
function stop_celery()
{
  docker stop celery-worker
}

# Delete celery container
function delete_celery_container()
{
  docker rm celery-worker -f
}

# Delete celery image
function delete_celery_image()
{
  docker rmi celery -f
  docker rmi $(docker images -f dangling=true -q)
}

# Build wordcounting app
function build_wordcounter()
{
  docker build -f ./Dockerfile.wordcounter -t wordcounter .
}

# Run wordcounting app
function run_wordcounter()
{
  docker run -d -p 5000:5000 --name wordcounter_app --net=redis-celery --rm=false wordcounter
}

$@
