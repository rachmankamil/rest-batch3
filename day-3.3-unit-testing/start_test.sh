export FLASK_ENV=Testing
pytest -v --cov=blueprint tests/
export FLASK_ENV=Development