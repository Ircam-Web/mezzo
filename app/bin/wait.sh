#!/bin/sh

set -e

port=$(env | grep POSTGRES_PORT | cut -d = -f 2)

echo -n "waiting for TCP connection to $host:$port..."

while ! nc -w 1 db $port 2>/dev/null
do
  echo -n .
  sleep 1
done

echo 'ok'
