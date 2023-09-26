help:
	@ echo ''
	@ echo 'Usage: make [TARGET]'
	@ echo 'Targets:'
	@ echo '  create-venv           create venv and activate and upgrade pip'
	@ echo '  install-requirements  install requirements project'
	@ echo '  migrate-database		migrate database'
	@ echo '  run-tests             run all tests file'
	@ echo '  run-server            run server on port 8000'
	@ echo '  help'

create-venv:
	@ python -m venv env
	@ source ./env/bin/activate
	@ python -m pip install --upgrade pip

install-requirements:
	@ python -m pip install -r ./requirements.txt

migrate-database:
	@ python manage.py makemigrations
	@ python manage.py migrate

run-tests:
	@ python manage.py test

run-server:
	@ python manage.py runserver
