# start.sh

export FLASK_APP=wsgi.py
export FLASK_DEBUG=1
export APP_CONFIG_FILE=config.py
export FLASK_ENV=development
flask run
