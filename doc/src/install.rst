
Install
=======

Clone
++++++

On Linux, first install Git_, Docker-engine_ and docker-compose_ and open a terminal.

On MacOS or Windows install Git_ and the Docker-Toolbox_ and open a Docker Quickstart Terminal.

Then run these commands::

    git clone --recursive https://github.com/yomguy/mezzanine-organization.git


Start
+++++

Our docker composition already bundles some powerful containers and bleeding edge frameworks like: Nginx, MySQL, Redis, Celery, Django and Python. It thus provides a safe and continuous way to deploy your project from an early development stage to a massive production environment.

For a production environment setup::

    cd mezzanine-organization
    docker-compose up

which builds, (re)creates, starts, and attaches all containers.

Then browse the app at http://localhost:8020/

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
