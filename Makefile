test:
	coverage run --branch --source=payline `which django-admin.py` test
	coverage report --omit=payline/test*,payline/migrations*
