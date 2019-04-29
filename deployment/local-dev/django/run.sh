#!/usr/bin/env bash

set -ex

pip3 install -r requirements.txt --cache-dir /pip-cache

python manage.py migrate

/usr/bin/supervisord -c /supervisord.conf
