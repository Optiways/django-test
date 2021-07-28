#!/bin/bash

make install
python manage.py collectstatic --noinput
make migrate
make run