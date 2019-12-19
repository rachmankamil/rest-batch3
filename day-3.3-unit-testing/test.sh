#! /bin/bash

clear && clear
export FLASK_ENV=testing
pytest --cov-fail-under=80 --cov=blueprints --cov-report html tests/
export FLASK_ENV=development