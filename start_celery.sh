#!/bin/bash
docker build -f ./Dockerfile.celery -t celery .

# docker build . -t 'celery'
docker run --name celery-worker celery
