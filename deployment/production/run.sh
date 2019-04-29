#!/usr/bin/env sh

python manage.py collectstatic --no-input

nginx &

uwsgi --ini uwsgi.ini --chmod-socket=666