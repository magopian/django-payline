Django-payline
==================

.. image:: https://secure.travis-ci.org/magopian/django-payline.png
   :alt: Build Status
   :target: https://secure.travis-ci.org/magopian/django-payline

Easily make payments using Payline_

.. _Payline: http://www.payline.com/

* Author: Mathieu Agopian and `contributors`_
* Licence: BSD
* Compatibility: Django 1.3+
* Requirements: suds_

.. _contributors: https://github.com/magopian/django-payline/contributors
.. _suds: http://pypi.python.org/pypi/suds/


Installation
------------

* ``pip install -U django-payline``
* Add ``payline`` to your ``INSTALLED_APPS``

For extensive documentation see the ``docs`` folder or `read it on
readthedocs`_

.. _read it on readthedocs: http://django-payline.readthedocs.org/

To install the `in-development version`_ of django-payline, run ``pip
install django-payline==dev``.

.. _in-development version: https://github.com/magopian/django-payline/tarball/master#egg=django-payline-dev

Help
----

Drop me a mail.

Bugs
----

Really? Oh well... Please Report. Or better, fix :)

Development
-----------

Thanks for asking!

Get the code::

    git clone git@github.com:magopian/django-payline.git
    cd django-payline
    virtualenv -p python2 env
    source env/bin/activate
    add2virtualenv .

Install the development requirements::

    pip install -r requirements.txt
    pip install django  # must be django 1.3 or above

Run the tests::

    DJANGO_SETTINGS_MODULE=payline.test_settings make test

By default, two integration tests will be skipped when running the tests. Those
integration tests need the following settings (put them in a
``settings.py`` file)::

    from test_settings import *


    PAYLINE_MERCHANT_ID = 'your payline merchant ID'
    PAYLINE_KEY = 'your payline API key'
    PAYLINE_VADNBR = 'your payline VAD number'

Then run the full test suite, including the integration tests::

    DJANGO_SETTINGS_MODULE=payline.settings make test
