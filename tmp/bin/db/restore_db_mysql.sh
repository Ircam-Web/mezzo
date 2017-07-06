#!/bin/bash

gunzip < /srv/backup/ircam_shops.sql.gz | mysql -hprestadb -uroot -pmysecretpassword ircam_shops
echo "Restore done!"
