run: ## Run the test server.
	python manage.py runserver_plus

install: ## Install the python requirements.
	pip install -r requirements.txt

migrate: ## Generate and apply migrations.
	python manage.py makemigrations
	python manage.py migrate

superuser: ## Create a superuser.
	python manage.py createsuperuser

test: ## Run the tests.
	python manage.py test