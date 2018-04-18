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
