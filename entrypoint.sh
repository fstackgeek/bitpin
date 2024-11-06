#!/bin/sh

set -e

echo "Making migrations..."
python manage.py makemigrations
echo "Done"

echo "Performing migrations..."
python manage.py migrate
echo "Done"

exec "$@"
