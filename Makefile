PORT?=8000

create-env:
	sudo apt-get install autoconf automake libtool
	sudo bash install-coap-client.sh
	virtualenv venv --python=python3 --system-site-packages
	./venv/bin/pip install -r requirements.txt

create-env-pi:
	make create-env
	./venv/bin/pip install -r requirements_rpi.txt

start:
	./venv/bin/python manage.py migrate
	./venv/bin/python manage.py collectstatic --noinput
	google-chrome http://0.0.0.0:${PORT}/ &
	./venv/bin/python manage.py runserver 0.0.0.0:${PORT}
