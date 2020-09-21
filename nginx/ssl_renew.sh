#!/bin/bash

COMPOSE="/usr/bin/docker-compose --no-ansi"
DOCKER="/usr/bin/docker"

cd /home/sawy89/RasPierreUnchained
$COMPOSE run certbot renew --dry-run && $COMPOSE kill -s SIGHUP ras_nginx
$DOCKER system prune -af