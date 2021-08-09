run: ## Run the test server.
	python manage.py runserver_plus

migrate: ## Run project's migrations
	python manage.py migrate

install: ## Install the python requirements.
	pip install -r requirements/dev.txt
