#!/bin/bash

# paths
app='/srv/app'
manage=$app'/manage.py'
wsgi=$app'/wsgi.py'
static='/srv/static/'
media='/srv/media/'
src='/srv/src/'
log='/var/log/uwsgi/app.log'

# uwsgi params
port=8000
processes=8
threads=16
autoreload=3
uid='www-data'
gid='www-data'
# patterns='*.js;*.css;*.jpg;*.jpeg;*.gif;*.png;*.svg;*.ttf;*.eot;*.woff;*.woff2'

# Staging
# pip install pandas xlwt
# pip install -U https://forge.ircam.fr/p/django-eve/source/download/dev/
# pip install https://forge.ircam.fr/p/django-prestashop/source/download/master/ --src /srv/lib
# pip install -U https://github.com/stephenmcd/grappelli-safe/archive/dynamic_stacked.zip
# pip install django-querysetsequence==0.6.1 django==1.9.11
# pip install django-autocomplete-light django-querysetsequence
# /usr/bin/yes | pip uninstall django-orderable

chown -R $uid:$gid $media

# waiting for other services
sh $app/bin/wait.sh

# django setup
python $manage wait-for-db

# initial setup
if [ ! -f .init ]; then
    bash $app/bin/init.sh
    touch .init
fi

# app start
if [ "$1" = "--runserver" ]; then
    python $manage runserver 0.0.0.0:8000
else
    # static files auto update
    # watchmedo shell-command --patterns="$patterns" --recursive \
    #     --command='python '$manage' collectstatic --noinput' $app &

    python $manage collectstatic --noinput

    uwsgi --socket :$port --wsgi-file $wsgi --chdir $app --master \
    --processes $processes --threads $threads \
    --uid $uid --gid $gid --logto $log --touch-reload $wsgi
fi
