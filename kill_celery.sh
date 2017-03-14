docker stop celery-worker
docker rm celery-worker -f
docker rmi celery -f
docker rmi $(docker images -f dangling=true -q)
