run: ## Run the test server.
	python manage.py runserver_plus

install: ## Install the python requirements.
	pip install -r requirements.txt

migrate: ## Run the test server.
	python manage.py migrate
