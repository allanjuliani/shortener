#!/bin/bash

NAME="shortener"
DJANGO_WSGI_MODULE="${NAME}.wsgi"
USER="django"
PORT="8000"
ADDRESS="0.0.0.0:${PORT}"
WORKERS=2
THREADS=2

echo "Starting $NAME at $ADDRESS"

exec python -m gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name ${NAME} \
  --workers ${WORKERS} \
  --threads ${THREADS} \
  --user ${USER} \
  --bind ${ADDRESS}
