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
	@ python3 -m venv env
	@ source ./env/bin/activate
	@ python3 -m pip install --upgrade pip

install-requirements:
	@ python3 -m pip install -r ./requirements.txt

migrate-database:
	@ python3 manage.py makemigrations
	@ python3 manage.py migrate

run-tests:
	@ python3 manage.py test

run-server:
	@ python3 manage.py runserver