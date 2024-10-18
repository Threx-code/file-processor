startapp:
	@if [ -z "$(name)" ]; then \
  		echo "Error: You must provide the app. Usage: make app name_of_app"; \
	else \
		python manage.py startapp $(name); \
	fi

migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate
