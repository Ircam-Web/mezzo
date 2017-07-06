#!/bin/sh

docker-compose run app python manage.py makemessages -a
docker-compose run app python manage.py compilemessages
