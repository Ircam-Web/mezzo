FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir /srv/app
RUN mkdir /srv/lib
WORKDIR /srv

RUN apt-get update && apt-get install -y apt-transport-https
COPY ../etc/apt/sources.list /etc/apt/
COPY ../requirements.txt /srv
RUN apt-get update && \
    DEBIAN_PACKAGES=$(egrep -v "^\s*(#|$)" /srv/requirements.txt) && \
    apt-get install -y --force-yes $DEBIAN_PACKAGES && \
    echo fr_FR.UTF-8 UTF-8 >> /etc/locale.gen && \
    locale-gen && \
    apt-get clean

ENV LANG fr_FR.UTF-8
ENV LANGUAGE fr_FR:fr
ENV LC_ALL fr_FR.UTF-8

COPY package.json /srv
RUN npm install
RUN npm install -g gulp
RUN npm install -g bower

COPY Gemfile /srv
RUN gem install bundler
RUN bundle install

COPY requirements.txt /srv
RUN pip install -r requirements.txt --src /srv/lib

WORKDIR /srv/app
