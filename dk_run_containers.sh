var=$(docker ps -a -q)
if [ -n "$var" ]; then
  $(docker stop $var)
  $(docker rm $var)
fi

# docker run -i -t -d -p 5000:5000 --name="flask_app" word_count_docker /bin/bash
# docker run -t -d word_count_docker /bin/bash
docker run -d -p 5000:5000 --name="flask_app" word_count_docker
