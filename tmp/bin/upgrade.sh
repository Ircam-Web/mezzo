#!/bin/sh

git pull
git submodule foreach git pull
docker-compose run app python /srv/app/manage.py migrate
# docker-compose run app python /srv/app/manage.py update_translation_fields
docker-compose run app bash -c "cd /srv && bower --allow-root install && gulp build"
docker-compose run app python /srv/app/manage.py collectstatic --noinput
docker-compose run app bash /srv/doc/build.sh
touch app/wsgi.py
