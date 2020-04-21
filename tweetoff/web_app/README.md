# twitoff

## Installation

TODO: instructions

## Setup

TODO: instructions

Migrate the db:

```sh
FLASK_APP=web_app flask db init
FLASK_APP=web_app flask db migrate
FLASK_APP=web_app flask db upgrade
```

## Usage

```sh
# Mac:
FLASK_APP=web_app flask run

# Windows:
export FLASK_APP=web_app # one-time thing, to set the env var
flask run
```
