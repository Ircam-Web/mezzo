=====
Mezzo
=====

Mezzo is a complete CMS for organizations with complex workflows

It is based on Mezzanine_ and Django_.

Use cases
==========

In fact any organization web site that needs a dedicated customable backend...

Features
========

- Page, news and event management
- Smart media management (video, audio, etc..)
- Project data management including demo repositories
- Activity management of person per department
- Job candidancy forms
- Full translation models
- Fully dockerized for easy setup

.. _Django : https://www.djangoproject.com/
.. _Mezzanine : http://mezzanine.jupo.org/

Architecture
============

For easier development and production workflow, this application has been dockerized.

Paths
++++++

- app \
    django application

  - app/locale \
        locales for translations
  - app/migrations \
        mezzanine migrations
  - app/organization \
        organization app
  - app/bin \
        commands to run app with docker
  - app/static \
        all assets, js, css files
  - app/templates \
        main templates

- bin \
    maintenance bin
- env \
    docker-compose environment files
- etc \
    custom config files
- lib \
    custom libraries added as git submodules
- var \
    all application data versioned on a separated repository

  - var/backup \
        database backup directory
  - var/media \
        all media uploaded through the app
  - var/lib/postgresql \
        postgresql DB (not versioned)
  - var/log/nginx \
        nginx logs (not versioned)
  - var/log/uwsgi \
        uwsgi logs (not versioned)

- bower.json \
    javascript dependencies
- debian-requirements.txt \
    used by docker to install debian packages
- docker-compose.yml \
    configuration file for docker containers used by docker-compose
- Dockerfile \
    instructions to build the app image
- Gemfile \
    gem dependecies for ruby. For our case, it will install _Sass and _Compass.
- gulpfile.js \
    script to compile all CSS and JS files
- install.py \
    daemon and init boot script installer (Linux only)
- package.json \
    gulp dependencies when running "gulp install"
- requirements-dev.txt \
    application package in dev version
- requirements.txt \
    application package



Models
++++++

Main modules embed in app/organization

- agenda \
    manage events, using _Mezzanine-Agenda
- core \
    commons or abstract functionnality
- formats \
    manage date format
- job \
    jobs and candidacies for residency
- magazine \
    all news are managed by topics, articles and briefs
- media \
    audio and video gathered in playlist
- network \
    create a tree of Organizations > Departments > Teams > Persons
- pages \
    managing diffent type of pages (admin/pages/page/) and home
- projects \
    represent projects related to a team or a person
- shop \
    manage product from prestashop (softwares and subscriptions), using _Cartridge


.. _Compass : http://compass-style.org/
.. _Sass: http://sass-lang.com/

Install
=======

Clone
++++++

On Linux, first install Git_, Docker-engine_ and docker-compose_ and open a terminal.

On MacOS or Windows install Git_ and the Docker-Toolbox_ and open a Docker Quickstart Terminal.

Then run these commands::

    git clone --recursive https://github.com/Ircam-Web/mezzo.git


Start
+++++

Our docker composition already bundles some powerful containers and bleeding edge frameworks like: Nginx, MySQL, Redis, Celery, Django and Python. It thus provides a safe and continuous way to deploy your project from an early development stage to a massive production environment.

For a production environment setup::

    cd mezzanine-organization
    docker-compose up

which builds, (re)creates, starts, and attaches all containers.

Then browse the app at http://localhost:8021/

On MacOS or Windows, we need to replace 'localhost' by the IP given by the docker terminal.

.. warning :: Before any serious production usecase, you *must* modify all the passwords and secret keys in the configuration files of the sandbox.


Daemonize
+++++++++++

The install the entire composition so that it will be automatically run at boot and in the background::

    sudo bin/install.py

options::

    --uninstall : uninstall the daemon
    --cron : install cron backup rule (every 6 hours)
    --user : specify user for cron rule
    --systemd : use systemd
    --composition_file : the path of the YAML composition file to use (optional)

This will install a init script in /etc/init.d. For example, if your app directory is named `mezzanine-organization` then `/etc/init.d/mezzanine-organization` becomes the init script for the OS booting procedure and for you if you need to start the daemon by hand::

    sudo /etc/init.d/mezzanine-organization start


.. _Docker-engine: https://docs.docker.com/installation/
.. _docker-compose: https://docs.docker.com/compose/install/
.. _docker-compose reference: https://docs.docker.com/compose/reference/
.. _Docker-Toolbox: https://www.docker.com/products/docker-toolbox
.. _Git: http://git-scm.com/downloads
.. _NodeJS: https://nodejs.org
.. _Gulp: http://gulpjs.com/
.. _Mezzanine-Agenda : https://github.com/jpells/mezzanine-agenda
.. _Cartridge : https://github.com/stephenmcd/cartridge/

Development
===========

Dev mode
+++++++++

For a development environment setup::

    docker-compose -f docker-compose.yml -f env/dev.yml up

This will launch the django development server. Then browse the app at http://localhost:9021/

On MacOS or Windows, we need to replace 'localhost' by the IP given by the docker terminal.

.. warning :: In this mode, Django is run with the `runserver` tool in DEBUG mode. NEVER use this in production!


Back
+++++

If you modify or add django models, you can produce migration files with::

    bin/makemigrations.sh

To apply new migrations::

    bin/migrate.sh

Accessing the app container shell::

    docker-compose run app bash


Front
+++++

The styles are written in SASS in app/static and the builder uses Gulp.
All the builing tools are included in the app container so that you can build the front in one command::

    bin/build_font.sh

To start the gulp server to get dynamic builing::

    docker-compose run app gulp serve

Gulp will launch BrowserSync. BrowserSync is a middleware that expose the website on port 3000.
Any change on CSS or JS files will trigger the build system and reload the browser.
Maintenance
============

Log
++++

- var/log/nginx/app-access.log \
    nginx access log of the app
- var/log/nginx/app-error.log \
    nginx error log of the app
- var/log/uwsgi/app.log \
    uwsgi log of the app


Backup & restore
+++++++++++++++++

To backup the database and all the media, this will push all of them to the var submodule own repository::

    bin/push.sh

.. warning :: use this ONLY from the **production** environment!

To restore the backuped the database, all the media and rebuild front ()::

    bin/pull.sh

.. warning :: use this ONLY from the **development** environment!


Upgrade
+++++++++

Upgrade application, all dependencies, data from master branch and also recompile assets::

    bin/upgrade.sh


Repair
+++++++

If the app is not accessible, first try to restart the composition with::

    docker-compose restart

If the app is not responding yet, try to restart the docker service and then the app::

    docker-compose stop
    sudo /etc/init.d/docker restart
    docker-compose up

If the containers are still broken, try to delete exisiting containers (this will NOT delete critical data as database or media)::

    docker-compose stop
    docker-compose rm
    docker-compose up

In case you have installed the init script to run the app as a daemon (cf. section "Daemonize"), you can use it to restart the app:

    /etc/init.d/mezzanine-organization restart

If you need more informations about running containers::

    docker-compose ps

Or more, inspecting any container of the composition (usefully to know IP of a container)::

    docker inspect [CONTAINER_ID]

Copyrights
==========

* Copyright (c) 2016 Ircam
* Copyright (c) 2016 Guillaume Pellerin
* Copyright (c) 2016 Emilie Zawadzki
* Copyright (c) 2016 Jérémy Fabre

License
========

mezzanine-organization is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

mezzanine-organization is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

Read the LICENSE.txt file for more details.
