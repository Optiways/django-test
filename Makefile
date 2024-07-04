run: ## Run the test server.
	python3 manage.py runserver_plus

install: ## Install the python requirements.
	pip install -r requirements.txt

migrate: ## Install the python requirements.
	python3 manage.py migrate
