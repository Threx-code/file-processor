build:
	docker-compose build

fresh_build:
	docker-compose build --no-cache

start:
	docker-compose up -d

stop:
	docker-compose down

restart:
	docker-compose down
	docker-compose up -d

logs:
	docker-compose logs -f

start_app:
	docker exec -it app /bin/sh

makeapp:
	docker exec -it app python manage.py startapp $(app_name)


startproject:
	docker exec -it app django-admin startproject $(project_name) .

makemigration:
	docker exec -it app python manage.py makemigrations

migrate:
	docker exec -it app python manage.py migrate

secret_key:
	docker exec -it app python manage.py shell -c "from django.core.management import utils; print(utils.get_random_secret_key())"

rand_key:
	openssl rand -base64 $(key_length)