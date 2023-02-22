PROJECT_NAME := $(shell basename $(shell pwd))
WORK_DIR := /app
RUN := run -it --rm
VOLUME := -v ${PWD}:$(WORK_DIR)
PORT := -p 8000:8000

run: ## Run the test server.
	python manage.py runserver_plus

install: ## Install the python requirements.
	pip install -r requirements.txt

build:
	docker build -t $(PROJECT_NAME) .

start:
	docker $(RUN) $(VOLUME) $(PORT) $(PROJECT_NAME)

migrate:
	docker $(RUN) $(VOLUME) $(PROJECT_NAME) /bin/bash -c "./manage.py migrate"

init: build migrate start

shell:
	docker $(RUN) $(VOLUME) $(PROJECT_NAME) /bin/bash -c "./manage.py shell+"

container:
	docker $(RUN) $(VOLUME) $(PROJECT_NAME) /bin/bash

dev-container:
	docker $(RUN) $(VOLUME) $(PROJECT_NAME) /bin/bash -c "zsh"
