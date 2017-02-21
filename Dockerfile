FROM ubuntu:16.04
 # Install system level requirements
 RUN apt-get update -y && \
     apt-get install -y python-pip python-dev

RUN apt-get install -y postgresql postgresql-server-dev-9.5

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /word_count/requirements.txt

WORKDIR /word_count

RUN pip install -r requirements.txt
COPY . /word_count

#ENV APP_SETTINGS "config.DevelopmentConfig"
#ENV DATABASE_URL "postgresql://postgres:postgres@localhost/wordcount_dev"

ENTRYPOINT [ "python" ]
EXPOSE 5000
CMD ["manage.py", "runserver", "--host", "0.0.0.0" ]
