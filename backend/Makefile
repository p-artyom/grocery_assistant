MANAGE = python manage.py

run:
	$(MANAGE) runserver

style:
	black -S -l 79 .
	isort .
	flake8 .

shell:
	$(MANAGE) shell

testp:
	$(MANAGE) test posts

testa:
	$(MANAGE) test about

testu:
	$(MANAGE) test users