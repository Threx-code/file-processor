install_all:
	dpip install -r requirements.txt

appinstall:
	app pip install $(package)

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

rand_key:
	openssl rand -base64 $(key_length)