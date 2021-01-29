#!/bin/bash

export DJANGO_DATABASE_NAME=local
export DJANGO_DATABASE_USER=root
export DJANGO_DATABASE_PASSWORD=
export DJANGO_DATABASE_HOST=127.0.0.1
export DJANGO_DATABASE_PORT=3306

python app_microservice/manage.py runserver
