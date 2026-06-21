#!/bin/sh
set -eu

case "${DJANGO_SETTINGS_MODULE:-}" in
    configuration.settings.beta|configuration.settings.prod)
        ;;
    *)
        echo >&2 \
            "Docker requires configuration.settings.beta or configuration.settings.prod."
        exit 64
        ;;
esac

python manage.py migrate --noinput
python manage.py collectstatic --noinput --clear

exec "$@"