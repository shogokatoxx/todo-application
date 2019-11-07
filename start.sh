#!/bin/sh

set -xe

pipenv run python manage.py migrate && pipenv run python manage.py runserver
