run: ## Run the test server.
	python manage.py runserver_plus

migrate: ## Migrate django models
	python manage.py migrate

install: ## Install the python requirements.
	pip install -r requirements.txt
