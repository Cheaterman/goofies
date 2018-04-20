#!/usr/bin/env sh

WSGI_PORT=${1:-5000}
WEB_PORT=${2:-8080}
APPLICATION=${3:-$(basename $(pwd))}

docker-compose exec $APPLICATION bash -c ". /env/bin/activate && cd /code/${APPLICATION} && FLASK_APP=__init__.py flask db upgrade && exit"

uwsgi --master --http :$WEB_PORT --http-to :$WSGI_PORT
