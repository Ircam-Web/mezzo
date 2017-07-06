#!/bin/sh

docker-compose run app python /srv/app/manage.py poll_twitter --force
