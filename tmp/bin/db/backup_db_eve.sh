#!/bin/bash

pg_dump -hpgdb -Upostgres eve | gzip > /srv/backup/eve.sql.gz
