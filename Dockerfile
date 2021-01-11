FROM python:3.7-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /srv

RUN apt-get update && apt-get install -y apt-transport-https
COPY etc/apt/sources.list /etc/apt/
COPY etc/apt/preferences.d/nodejs /etc/apt/preferences.d/
COPY requirements.txt /srv
RUN apt-get update && \
    DEBIAN_PACKAGES=$(egrep -v "^\s*(#|$)" /srv/requirements.txt) && \
    apt-get install -y --force-yes $DEBIAN_PACKAGES && \
    echo fr_FR.UTF-8 UTF-8 >> /etc/locale.gen && \
    locale-gen && \
    apt-get clean

ENV LANG fr_FR.UTF-8
ENV LANGUAGE fr_FR:fr
ENV LC_ALL fr_FR.UTF-8

RUN npm install -g gulp
RUN npm install -g bower

RUN pip install -U pip
RUN pip install -U setuptools

RUN mkdir /srv/app
COPY app/requirements.txt /srv/app
RUN pip install -r app/requirements.txt

RUN mkdir /srv/lib
COPY lib /srv/lib
COPY bin/build/local/setup_lib.sh /srv
RUN bash setup_lib.sh

WORKDIR /srv/app
