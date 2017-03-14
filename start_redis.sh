# -d -p allows to port host ip to docker
docker run -d -p 6379:6379 --name redis-server -d redis
