#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
      sleep 0.1
    done
fi

python manage.py flush --no-input
python manage.py migrate

exec "$@"