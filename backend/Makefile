MANAGE = python manage.py

run:
	$(MANAGE) runserver

style:
	black -S -l 79 .
	isort .
	flake8 .

super:
	$(MANAGE) createsuperuser

makemig:
	$(MANAGE) makemigrations

mig:
	$(MANAGE) migrate

import:
	$(MANAGE) importcsv

test:
	$(MANAGE) test
