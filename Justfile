default:
    @just --list --unsorted

setup:
    @poetry install

run:
    @poetry run uvicorn run:app --port 8080
