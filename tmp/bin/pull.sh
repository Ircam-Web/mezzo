#!/bin/sh

sudo chown -R $USER var/media
sudo chown -R $USER var/backup
git pull
git submodule foreach git pull origin master
docker-compose run db /srv/bin/db/restore.sh
docker-compose run app bash -c "cd /srv && bower --allow-root install && gulp build"
