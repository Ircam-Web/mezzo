#!/bin/bash

export PGPASSWORD=$POSTGRES_PASSWORD

pg_restore -c -Fc -hdb -Upostgres -dpostgres /srv/backup/postgres.dump

echo "Restore done!"
