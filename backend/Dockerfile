# syntax=docker/dockerfile:1.7

ARG PYTHON_IMAGE=python:3.14.6-slim-bookworm

FROM ${PYTHON_IMAGE} AS dependencies

ARG POETRY_VERSION=2.4.1

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=0 \
    VIRTUAL_ENV="/opt/venv" \
    PATH="/opt/venv/bin:${PATH}"

WORKDIR /build

# Poetry is a build-only dependency and is not copied to the runtime image.
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install "poetry==${POETRY_VERSION}" \
    && python -m venv "${VIRTUAL_ENV}"

COPY pyproject.toml poetry.lock ./

RUN --mount=type=cache,target=/root/.cache/pypoetry \
    poetry install --only main --no-root --no-ansi


FROM ${PYTHON_IMAGE} AS runtime

LABEL org.opencontainers.image.title="blendesflow-backend" \
      org.opencontainers.image.description="Django REST Framework served by Gunicorn" \
      org.opencontainers.image.source="blendesflow"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PATH="/opt/venv/bin:${PATH}" \
    DJANGO_SETTINGS_MODULE="configuration.settings.beta" \
    GUNICORN_CMD_ARGS="--bind=0.0.0.0:8000 --workers=3 --threads=2 --worker-tmp-dir=/dev/shm --timeout=60 --graceful-timeout=30 --keep-alive=5 --max-requests=1000 --max-requests-jitter=100 --no-control-socket --access-logfile=- --error-logfile=- --capture-output"

WORKDIR /app

RUN groupadd --gid 10001 django \
    && useradd --uid 10001 --gid django \
        --no-create-home --home-dir /nonexistent \
        --shell /usr/sbin/nologin django \
    && mkdir -p /var/www/static /var/www/media \
    && chown django:django /var/www/static /var/www/media \
    && chmod 0755 /var/www/static /var/www/media

COPY --from=dependencies /opt/venv /opt/venv
COPY . /app
COPY --chmod=0555 docker-entrypoint.sh /usr/local/bin/docker-entrypoint

USER 10001:10001

# Internal Docker network only. Do not publish this port on the host.
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["python", "-c", "import socket; connection = socket.create_connection(('127.0.0.1', 8000), timeout=3); connection.close()"]

STOPSIGNAL SIGTERM

ENTRYPOINT ["docker-entrypoint"]
CMD ["gunicorn", "configuration.wsgi:application"]
