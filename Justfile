default:
    @just --list --unsorted

setup:
    @poetry install

run:
    @poetry run alembic upgrade head
    @poetry run uvicorn run:app --port 8080

db-migrate:
    #/bin/bash
    poetry run alembic revision --autogenerate -m "add user schema" && \
    poetry run alembic upgrade head

run-db:
    podman run --rm \
        -e POSTGRESQL_USERNAME=pythops \
        -e POSTGRESQL_PASSWORD=pythops \
        -e POSTGRESQL_DATABASE=pythops \
        -p 5432:5432 \
        bitnami/postgresql:latest
