run: ## Run the test server.
	python manage.py runserver_plus 0.0.0.0:8000

install: ## Install the python requirements.
	pip install -r requirements.txt

migrate: ## Execute Django migrations
	python manage.py migrate
