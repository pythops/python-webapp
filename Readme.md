# Python Web App Structure

This is the demo app for the article [Python Web App Structure](https://pythops.com/post/python-web-app-structure.html)

## Prerequisites

You need:

- [python](https://www.python.org/)
- [httpie](https://github.com/httpie)
- [podman](https://github.com/containers/podman)
- [poetry](https://github.com/python-poetry/poetry)
- [just](https://github.com/casey/just)

## Setup

1. Start a postrges instance with podman

```shell
$ just run-db
```

2. Run the web app

```shell
$ just run

```

3. Check the API doc here http://127.0.0.1:8080/docs

## API

#### Create a new user

```bash
$ http POST :8080/users username="pythops" email="contact@pythops.com"
```

#### Get all users

```shell
$ http :8080/users

```

## License

AGPLv3
