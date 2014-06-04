test:
	coverage run --branch --source=payline `which django-admin.py` test
	coverage report --omit=payline/test*,payline/migrations*

translate:
	cd payline && django-admin.py makemessages --settings=payline.settings -a

install-deps:
	pip install -r requirements.txt

clean:
	find . -name "*.pyc" -delete
