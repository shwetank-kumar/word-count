#!/bin/bash
function start_redis()
{
  docker run -d -p 6379:6379 --name redis-server -d redis
}

function build_celery()
{
    docker build -f ./Dockerfile.celery -t celery .
}

function run_celery()
{
  docker run --name celery-worker --rm=false celery
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

$@
