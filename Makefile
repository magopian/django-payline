test:
	coverage run --branch --source=payline `which django-admin.py` test
	coverage report --omit=payline/test*,payline/migrations*

translate:
	cd payline && django-admin.py makemessages --settings=payline.settings -a
