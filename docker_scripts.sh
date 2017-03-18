#!/bin/bash
function create_network()
{
  docker network create redis-celery
}

function start_redis()
{
  docker run -d -p 6379:6379 --name redis-server --net=redis-celery redis
  # docker run -d -p 6379:6379 --name redis-server redis
}

function stop_redis()
{
  docker stop redis-server
}

function delete_redis_container()
{
  docker rm redis-server
}

function delete_redis_image()
{
  docker rmi redis
}

function build_celery()
{
    docker build -f ./Dockerfile.celery -t celery .
}

function run_celery()
{
  docker run --name celery-worker --net=redis-celery --rm=false celery
  # docker run --name celery-worker celery
}

function start_celery()
{
  docker start celery-worker
}

function stop_celery()
{
  docker stop celery-worker
}

function delete_celery_container()
{
  docker rm celery-worker -f
}

function delete_celery_image()
{
  docker rmi celery -f
  docker rmi $(docker images -f dangling=true -q)
}

function build_wordcounter()
{
  docker build -f ./Dockerfile.wordcounter -t wordcounter .
}

function run_wordcounter()
{
  docker run -d -p 5000:5000 --name wordcounter_app --net=redis-celery --rm=false wordcounter
  # docker run --name celery-worker celery
}

$@
