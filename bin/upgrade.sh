#!/bin/sh

# Use this script to update a dev/prod server

git pull
git submodule foreach git pull
docker-compose run app python /srv/app/manage.py migrate
# docker-compose run app python /srv/app/manage.py update_translation_fields
bower install
gulp build
docker-compose run app python /srv/app/manage.py collectstatic --noinput
docker-compose run app bash /srv/app/doc/build.sh
