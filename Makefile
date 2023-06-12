run: ## Run the test server.
	python manage.py runserver_plus

install: ## Install the python requirements.
	pip install -r requirements.txt

migrate: ## Make migrations
	python manage.py migrate

makemigrations: ## Generate database migrations from models state
	python manage.py makemigrations