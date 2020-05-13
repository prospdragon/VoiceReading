# start.bat

set FLASK_APP=wsgi.py
set FLASK_DEBUG=1
set APP_CONFIG_FILE=config.py
set FLASK_ENV=development
flask run
