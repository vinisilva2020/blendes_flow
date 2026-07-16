#!/bin/sh
set -eu

case "${DJANGO_SETTINGS_MODULE:-}" in
    configuration.settings.docker|configuration.settings.production)
        ;;
    *)
        echo >&2 \
            "Docker requires configuration.settings.docker or configuration.settings.production."
        exit 64
        ;;
esac

python manage.py migrate --noinput
python manage.py collectstatic --noinput --clear

exec "$@"
