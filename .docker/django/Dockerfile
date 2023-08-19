# https://hub.docker.com/_/python
FROM python:3.11-bullseye

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends
RUN apt-get install curl python3-dev default-libmysqlclient-dev build-essential -y

RUN python3 -m pip install --upgrade pip

RUN useradd -ms /bin/bash django

USER django

COPY . /home/django/shortener

WORKDIR /home/django/shortener

ENTRYPOINT [".docker/django/entrypoint.sh"]
