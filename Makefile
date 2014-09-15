test:
	coverage run --branch --source=payline `which django-admin.py` test
	coverage report --omit=payline/test*,payline/migrations*

translate:
	cd payline && django-admin.py makemessages --settings=payline.settings -a

install-deps:
	pip install -r requirements.txt
	pip install "Django>=1.3"
	pip install South

clean:
	find . -name "*.pyc" -delete
