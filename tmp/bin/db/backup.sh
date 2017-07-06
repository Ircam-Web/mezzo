#!/bin/bash

export PGPASSWORD=$POSTGRES_PASSWORD

pg_dump -Fc -hdb -Upostgres -dpostgres > /srv/backup/postgres.dump

echo "Backup done!"
