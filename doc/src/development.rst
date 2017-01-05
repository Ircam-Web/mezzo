
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
