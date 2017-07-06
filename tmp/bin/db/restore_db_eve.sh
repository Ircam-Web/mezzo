#!/bin/bash

export PGPASSWORD="q2nqzt0WGnwWé,256"

db_exists=`psql -hevedb -Ueve -lqt  | cut -d \| -f 1 | grep -w eve | wc -l`

#if [ ! $db_exists == 0 ]; then
#    psql -hpgdb -Ueve  -c 'drop database eve'
#fi

psql -hevedb -Ueve -c 'create role eve'
psql -hevedb -Ueve -c 'create role django'
#psql -hevedb -Ueve -c 'create database eve'
gunzip -c /srv/backup/eve.sql.gz | psql -hevedb -Ueve -q eve
