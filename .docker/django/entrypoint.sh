#!/bin/bash

pip install -r requirements.txt

./manage.py collectstatic --noinput
./manage.py migrate --settings=shortener.settings_prod

.docker/django/gunicorn.sh
