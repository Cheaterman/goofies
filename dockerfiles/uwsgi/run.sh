#!/bin/bash

if [ -n "$PYPI_PORT" ]; then
    PYPI_FLAGS="-i ${PYPI_PORT/tcp:/http:}/root/pypi/"
fi

if find /env -maxdepth 0 -empty | read v; then
    virtualenv /env

    /env/bin/pip install --upgrade pip setuptools

    /env/bin/pip install uwsgi $PYPI_FLAGS
fi

cd /code && /env/bin/pip install -r ${REQUIREMENTS_FILE:-requirements.txt} $PYPI_FLAGS

if [[ "$1" == "shell" ]]
then
    cd /code && . /env/bin/activate && FLASK_APP=${WSGI_MODULE%%:*}/__init__.py flask shell
elif [[ "$1" == "bash" ]]
then
    cd /code && . /env/bin/activate && FLASK_APP=${WSGI_MODULE%%:*}/__init__.py bash
else
    cd /code && /env/bin/uwsgi --virtualenv /env --chdir /code -w ${WSGI_MODULE:-wsgi:application} --uwsgi-socket 0.0.0.0:5000
fi
