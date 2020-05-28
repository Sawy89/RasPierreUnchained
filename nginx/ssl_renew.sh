#!/bin/bash

COMPOSE="/usr/local/bin/docker-compose --no-ansi"
DOCKER="/usr/bin/docker"

cd /home/sawy89/RaspierreUnchained
$COMPOSE run certbot renew --dry-run && $COMPOSE kill -s SIGHUP ras_nginx
$DOCKER system prune -af