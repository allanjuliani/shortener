build:
	@cp .env.example .env
	@docker-compose build

rebuild:
	@docker-compose down --remove-orphans
	@docker-compose build --no-cache

up:
	@docker-compose up -d

down:
	@docker-compose down

install:
	@make build
	@make up

start:
	@docker start django_shortener
	@docker start mysql_shortener
	@docker start nginx_shortener

stop:
	@docker stop django_shortener
	@docker stop mysql_shortener
	@docker stop nginx_shortener

restart:
	@make stop
	@make start

shortener-clean:
	@make down
	@docker image rm shortener_django
	@docker volume rm shortener_my-db

docker-clean:
	@make down
	@docker system prune -a
	@docker volume prune

test:
	@docker exec -it django_shortener python -m pytest -v apps

cov:
	@docker exec -it django_shortener python -m pytest -v apps --cov=apps

createsuperuser:
	@docker exec -it django_shortener python manage.py createsuperuser --noinput --settings=shortener.settings_prod

shell-django:
	@docker exec -it django_shortener /bin/bash

shell-mysql:
	@docker exec -it mysql_shortener /bin/bash

shell-nginx:
	@docker exec -it nginx_shortener /bin/bash
