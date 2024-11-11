install: ## Install the python requirements.
	pip install -r requirements.txt

migrate: ## Migrate django models
	python manage.py makemigrations
	python manage.py migrate

run: ## Run the test server.
	python manage.py runserver_plus