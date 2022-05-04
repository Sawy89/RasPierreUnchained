#!/bin/bash

echo 'inizio sh'
echo $(date)

cd "$(dirname "$0")"

# Create folder
mkdir -p ./_backup
mkdir -p ./_backup/log

docker-compose -f docker-compose.prod.yml down -v
docker-compose -f docker-compose.prod.yml up -d --build

echo $(date)
echo 'fine sh'