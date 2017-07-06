#!/bin/sh

docker-compose run app python /srv/app/manage.py build_themes --no-input
docker-compose run app python /srv/app/manage.py collectstatic --no-input
