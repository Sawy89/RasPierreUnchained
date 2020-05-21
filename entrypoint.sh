#!/bin/sh

# Check DB is operative
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for PostgreSQL start"

    until nc -z -v -w30 $SQL_HOST $SQL_PORT
    do
        echo "Waiting for database connection..."
        # wait for 5 seconds before check again
        sleep 5
    done

    echo "PostgreSQL started"
fi

# Apply migration if needed
python manage.py flush --no-input
python manage.py migrate

# load data
python manage.py loaddata data.json # dev

# Execute command in dockercompose
exec "$@"