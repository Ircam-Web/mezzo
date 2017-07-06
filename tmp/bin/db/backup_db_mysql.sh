#!/bin/bash

mysqldump -hdb -uroot -phyRob0otlaz4 ircam-www | gzip > /srv/backup/ircam-www.sql.gz
echo "Backup done!"
