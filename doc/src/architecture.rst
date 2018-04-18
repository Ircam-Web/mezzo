
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
