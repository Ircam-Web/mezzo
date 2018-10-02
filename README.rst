=====
Mezzo
=====

Mezzo is a complete CMS for organizations with complex workflows.

It includes the state-of-the-art of all modern web backend and frontend frameworks and many smart for easy development between teams.

It provides a development and a production environment for Mezzanine-Organization_ which is based on Mezzanine_ and Django_ plus many other modules.

Use cases
==========

- Institutional or corporate web sites with a lot of structural data
- Project web applications
- Any django based project thanks to the smart modular architecture

Features
========

- Smart and collaborative content management (Department, Page, News, Events, Media, Project, Job, etc.)
- Full Project data management including demo repositories
- Person activity management per department
- Translation ready models and templates
- Full modular architecture fir easy customization
- Smart docker environment and packaging for easy scalable deployment on every platform

Examples
========

IRCAM : https://www.ircam.fr
STARTS : https://www.starts.eu

.. _Mezzanine-Organization : https://github.com/Ircam-Web/mezzanine-organization
.. _Django : https://www.djangoproject.com/
.. _Mezzanine : http://mezzanine.jupo.org/

Architecture
============

For easier development and production workflow, this application has been fully dockerized.

Paths
++++++

- app \
    django application

  - app/migrations \
        mezzanine migrations
  - app/bin \
        commands to run the app inside docker containers

- bin \
    management tools
- doc
    documentation
- env \
    docker-compose environment files
- etc \
    custom configuration files
- lib \
    custom libraries added as git submodules including mezzanine-organization and mezzanine-organization-themes
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

- requirements.txt \
    debian package dependencies
- docker-compose.yml \
    composition file for docker containers used by docker-compose
- Dockerfile \
    instructions to build the docker image of the app


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

Install
=======

Clone
++++++

First install Git_, Docker-engine_ and docker-compose_ and open a terminal.

On MacOS or Windows, you will maybe ned to install Docker-Toolbox_ and open a Docker Quickstart Terminal.

Then run these commands::

    git clone --recursive https://github.com/Ircam-Web/Mezzo.git


Start
+++++

Our docker composition already bundles some powerful containers and bleeding edge frameworks like: Nginx, MySQL, Redis, Celery, Django and Python. It thus provides a safe and continuous way to deploy your project from an early development stage to a massive production environment.

For a production environment setup::

    cd Mezzo

Copy the local_settings sample::

    cp app/local_settings.py.sample app/local_settings.py

and edit your own local_settings, especially the SECRET_KEY parameter. Then::

    bin/prod/up.sh

which builds, (re)creates, starts, and attaches all containers.

Then browse the app at http://localhost:8040/

On MacOS or Windows, you maybe need to replace 'localhost' by the IP given by the docker terminal.

.. warning :: Before any serious production usecase, you *must* modify all the passwords and secret keys in the configuration files of the sandbox.


Daemonize
+++++++++++

The install the entire composition so that it will be automatically run at boot and in the background::

    sudo bin/install/install.py

options::

    --uninstall : uninstall the daemon
    --cron : install cron backup rule (every 6 hours)
    --user : specify user for cron rule
    --systemd : use systemd
    --composition_file : the path of the YAML composition file to use (optional)

This will install a init script in /etc/init.d. For example, if your app directory is named `mezzanine-organization` then `/etc/init.d/mezzanine-organization` becomes the init script for the OS booting procedure and for you if you need to start the daemon by hand::

    sudo /etc/init.d/mezzo start


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

    bin/dev/up.sh

This will launch the django development server. Then browse the app at http://localhost:9021/

On MacOS or Windows, we need to replace 'localhost' by the IP given by the docker terminal.

.. warning :: In this mode, Django is run with the `runserver` tool in DEBUG mode. NEVER use this in production!


Backend
++++++++

If you modify or add django models, you can produce migration files with::

    bin/dev/makemigrations.sh

To apply new migrations::

    bin/dev/migrate.sh

Accessing the app container shell::

    docker-compose run app bash


Front
+++++

The styles are written in SASS in app/static and the builder uses Gulp.
All the builing tools are included in the app container so that you can build the front in one command::

    bin/build/front.sh

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


Backup & restore the database
+++++++++++++++++++++++++++++

To backup the database and all the media, this will push all of them to the var submodule own repository::

    bin/prod/push_data.sh

.. warning :: use this ONLY from the **production** environment!

To restore the backuped the database, all the media and rebuild front ()::

    bin/dev/pull_data.sh

.. warning :: use this ONLY from the **development** environment!


Upgrade
+++++++++

Upgrade application, all dependencies, data from master branch and also recompile assets::

    bin/prod/upgrade.sh


Troubleshooting
+++++++++++++++

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
