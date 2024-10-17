run: ## Run the test server.
	python3 manage.py runserver_plus

migrate: ## Migrate django models
	python3 manage.py migrate

install: ## Install the python requirements.
	pip install -r requirements.txt
