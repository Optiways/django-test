run: ## Run the test server.
	python manage.py runserver_plus

install: ## Install the python requirements.
	pip install -r requirements.txt

run: ## Run migration
	python manage.py makemigrations && python manage.py migrate