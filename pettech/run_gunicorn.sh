#!/usr/bin/env sh
set -e
SERVICE=${SERVICE:-users}
export PYTHONPATH="/app/pettech:${PYTHONPATH}"
case "$SERVICE" in
  users)
    export DJANGO_SETTINGS_MODULE=pettech.settings_users
    MODULE=pettech.wsgi_users:application
    ;;
  jobs)
    export DJANGO_SETTINGS_MODULE=pettech.settings_jobs
    MODULE=pettech.wsgi_jobs:application
    ;;
  bookings)
    export DJANGO_SETTINGS_MODULE=pettech.settings_bookings
    MODULE=pettech.wsgi_bookings:application
    ;;
  web)
    export DJANGO_SETTINGS_MODULE=pettech.settings_web
    MODULE=pettech.wsgi:application
    ;;
  *)
    export DJANGO_SETTINGS_MODULE=pettech.settings
    MODULE=pettech.wsgi:application
    ;;
esac

if [ "${RUN_MIGRATIONS:-false}" = "true" ]; then
  # Wait for DB to be ready and run migrations
  MAX_RETRIES=${MAX_DB_RETRIES:-30}
  COUNT=0
  until python pettech/manage.py migrate --noinput; do
    COUNT=$((COUNT+1))
    if [ "$COUNT" -ge "$MAX_RETRIES" ]; then
      echo "Migrations failed after $COUNT attempts. Exiting."
      exit 1
    fi
    echo "DB not ready or migration failed, retrying in 2s... ($COUNT/$MAX_RETRIES)"
    sleep 2
  done
fi

exec python -m gunicorn "$MODULE" --bind 0.0.0.0:8000
