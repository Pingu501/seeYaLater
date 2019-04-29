#!/usr/bin/env sh

set -ex

python manage.py start_miner &

nginx &

uwsgi --ini uwsgi.ini --chmod-socket=666