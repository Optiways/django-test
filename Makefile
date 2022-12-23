
run: migrate## Run the test server.
	python3.7 manage.py runserver_plus

install: ## Install the python requirements.
	pip3.7 install -r requirements.txt

generate-migrations: ## Apply django migrations
	python3.7 manage.py  makemigrations

migrate: generate-migrations ## Apply django migrations
	python3.7 manage.py  migrate