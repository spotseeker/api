# SpotSeeker
[![CI](https://github.com/spotseeker/api/actions/workflows/ci.yml/badge.svg)](https://github.com/spotseeker/api/actions/workflows/ci.yml)
![coverage](coverage-badge.svg)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)



SpotSeeker is a mobile application designed for travelers to share their experiences through images, discover new places, share their location and recommendations with other travelers around the world.

## Requirements
- Python 3.11
- Virtualenv 20.21
- PostgreSQL

## Steps

Create Python virtual environment:
```bash
virtualenv venv -p python3.11
```

Activate the virtual environment
```bash
source venv/bin/activate
```

Install the dependencies:
```bash
pip install -r requirements/local.txt
```

Install pre-commit hooks:
```bash
pre-commit install
```

Run the project:
```bash
python manage.py runserver
```

## Run with Docker
You need to install [Docker desktop](https://www.docker.com/) in order to get all the packages to run docker container with compose.
Then you need to create the network for the application with:

    $ docker network create spotseeker-net

With the network created you must have to create a .env file follow the example `.env.evample`

Finally run the container:

    $ docker compose up --build

## Running tests with pytest

    $ pytest
### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

### Type checks

Running type checks with mypy:

    $ mypy spotseeker
