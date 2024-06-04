.PHONY: help install migrate run create_data create_buses create_drivers create_places create_users test

help:  ## Display this help.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install: ## Install the python requirements.
	pip install -r requirements.txt

migrate: ## Run database migrations.
	python manage.py makemigrations
	python manage.py migrate

run: ## Run the test server.
	python manage.py runserver_plus

create_data: ## Generate initial data.
	python manage.py create_data

create_buses: ## Generate bus data.
	python manage.py create_buses

create_drivers: ## Generate driver data.
	python manage.py create_drivers

create_places: ## Generate place data.
	python manage.py create_places

create_users: ## Generate user data.
	python manage.py create_users

test: ## Run tests with pytest
	pytest
