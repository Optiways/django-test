run: ## Run the test server.
	python manage.py runserver_plus

install: ## Install the python requirements.
	pip install -r requirements.txt

migrate: ## Migrate.
	python manage.py migrate

test: ## Run unit test.
	python manage.py test

black: # Code formatter
	black --line-length 79 --experimental-string-processing ./padam_django/apps/*

flake8: # Code linter
	flake8 --max-line-length 79 ./padam_django/apps/*

