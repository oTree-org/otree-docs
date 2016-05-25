.. _server-generic:

Server setup (advanced)
=======================

.. note::

    If you are just testing your app locally, you can use
    ``otree runserver``, which is simpler than the below steps.

We typically recommend oTree users to deploy to Heroku (see instructions :ref:`here <heroku>`),
because that is the simplest for people who are not experienced with web server administration.

However, you may prefer to run oTree on your own server. Reasons may include:

-  You do not want your server to be accessed from the internet
-  You will be launching your experiment in a setting where internet
   access is unavailable
-  You want full control over how your server is configured

oTree runs on top of Django, so oTree setup is the same as Django setup.
Django runs on a wide variety of servers, except getting it to run on
a Windows server like IIS may require extra work; you can find info about
Django + IIS online. Below, instructions are given for using Unix.

Database
--------

oTree's default database is SQLite, which is fine for local development,
but insufficient for production.
We recommend PostgreSQL, although you can also use MySQL, MariaDB, or any other database
supported by Django.

To use Postgres, first install Postgres, create a user (called ``postgres`` below),
and start your Postgres server. The instructions for doing the above depend on your OS.

Once that is done, you can create your database::

    $ psql -c 'create database django_db;' -U postgres

Now you should tell oTree to use Postgres instead of SQLite.
The default database configuration in ``settings.py`` is::

    DATABASES = {
        'default': dj_database_url.config(
            default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
        )
    }

However, instead of modifying the above line directly,
it's better to set the ``DATABASE_URL`` environment variable on your server::

    DATABASE_URL=postgres://postgres@localhost/django_db

(To learn what an "environment variable" is, see `here <http://superuser.com/a/284351>`__.)

Once ``DATABASE_URL`` is defined, oTree will use it instead of the default SQLite.
(This is done via `dj_database_url <https://pypi.python.org/pypi/dj-database-url>`__.)
Setting the database through an environment variable
allows you to continue to use SQLite locally (which is easier and more convenient).

Then, instead of installing ``requirements_base.txt``, install ``requirements.txt``.
This will install ``psycopg2``, which is necessary for using Postgres.

You may get an error when you try installing ``psycopg2``, as described
`here <http://initd.org/psycopg/docs/faq.html#problems-compiling-and-deploying-psycopg2>`__.

The fix is to install the ``libpq-dev`` and ``python-dev`` packages.
On Ubuntu/Debian, do:

.. code-block:: bash

    sudo apt-get install libpq-dev python-dev


Install Redis
-------------

You need to install Redis server and run it on its default port (6379).

- Windows: download and run the `MSI <https://github.com/MSOpenTech/redis/releases>`__.
- Mac: if using Homebrew, you can follow the instructions here: `here <http://richardsumilang.com/server/redis/install-redis-on-os-x/>`__.
- Ubuntu: download `here <https://launchpad.net/~chris-lea/+archive/ubuntu/redis-server>`__.

You can test if Redis is running as follows:

.. code-block:: python

    >>> import redis
    >>> r = redis.Redis()
    >>> r.ping()


Deploy your code
----------------

If you are using a remote webserver, you need to push your code there,
typically using Git.

Open your shell, and make sure you have committed any changes as follows:

.. code-block:: bash

    pip freeze > requirements_base.txt
    git add .
    git commit -am '[commit message]'

(If you get the message
``fatal: Not a git repository (or any of the parent directories): .git``
then you first need to initialize the git repo.)

Then do:

.. code-block:: bash

    $ git push [remote name] master

Where [remote name] is the name of your server's git remote.


Running the server
------------------

If you are just testing your app locally, you can use the usual ``runserver``
command.

However, when you want to use oTree in production, you need to run the
production server, which can handle more traffic. You should use a process
control system like Supervisord, and have it launch otree with the command
``otree runprodserver``.

This will run the ``collectstatic`` command, and then
launch the server as specified in the ``Procfile`` in your project's root
directory. The default ``Procfile`` launches the ``daphne`` server.
If you want to use another server like Nginx, you need to modify the
``Procfile``. (If you instead want to use Apache, consult the Django docs.)

.. warning::

    Prior to v0.5, oTree used ``gunicorn``.
    oTree 0.5 and later uses the ``daphne`` server.

Next steps
----------

Set up :ref:`Sentry <sentry>`.

Apache and MySQL on Windows (v0.4 only)
---------------------------------------

.. note::

    This section only applies to oTree 0.4.
    It has not been updated yet for the latest 0.5 release,
    which does not use WSGI.

In general windows is not recommended as a platform for deployment but there
exists an easy solution based on WAMP Stack.

WAMP
~~~~

`WAMP <http://www.wampserver.com/>`__ is web stack that includes Apache, MySQL and PHP.
For this walkthrough we will use 32-bits version of WampServer 3.
We will use default path for WAMP: ``C:\wamp``.
Keep in mind that both installation and Wamp manager files should be executed as Administrator.
If installation is successfull you should be able to launch Wamp manager and navigate to localhost.

Installing dependencies using a virtualenv
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Install virtualenv: ``pip install virtualenv``
- Navigate to folder with your apps ``cd C:\wamp\www\oTree``
- Create virtual environment: ``virtualenv venv``
- Activate virtual environment: ``venv\Scripts\activate.bat``
- Install modules required for oTree: ``pip install -r requirements_base.txt``
- Install compiled version of ``mod_wsgi`` module from `here <http://www.lfd.uci.edu/~gohlke/pythonlibs/#mod_wsgi>`__:
  ``pip``: ``pip install mod_wsgi-4.4.23+ap24vc9-cp27-cp27m-win32.whl``. Copy file ``venv\mod_wsgi.so`` into apache
  folder ``C:\wamp\bin\apache\apache2.4.17\modules``

.. note::

    You should install version of ``mod_wsgi`` that is compatible with version of your ``python``.
    Therefore choose correspondingly x86 or amd64 and Python2.* or Python 3.*
    when you download precompiled version of ``mod_wsgi``.

- Install compiled version of ``mysql-python`` module from `here <http://www.lfd.uci.edu/~gohlke/pythonlibs/#mysql-python>`__:
  ``pip install MySQL_python-1.2.5-cp27-none-win32.whl``

Update Apache conf
~~~~~~~~~~~~~~~~~~

- Add following line to ``C:\wamp\bin\apache\apache2.4.17\conf\httpd.conf`` after all ``LoadModule ...`` statements:

.. code-block:: apacheconf

    WSGIPythonHome C:\Python27
    WSGIPythonPath C:\wamp\www\oTree\venv\Lib\site-packages;C:\wamp\www\oTree
    LoadModule wsgi_module modules/mod_wsgi.so

- Add following lines to very end of file ``C:\wamp\bin\apache\apache2.4.17\conf\httpd.conf``:

.. code-block:: apacheconf

    <VirtualHost *>
        Alias /static/ C:/wamp/www/oTree/_static_root/

        <Directory C:/wamp/www/oTree/static>
        Require all granted
        </Directory>

        WSGIScriptAlias / C:/wamp/www/oTree/wsgi.py

        <Directory C:/wamp/www/oTree>
        <Files wsgi.py>
        Require all granted
        </Files>
        </Directory>
    </VirtualHost>

Setup oTree
~~~~~~~~~~~

- create entering point script for oTree apps ``C:\wamp\www\oTree\wsgi.py``:

.. code-block:: python

    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

    from django.core.wsgi import get_wsgi_application
    from whitenoise.django import DjangoWhiteNoise

    application = get_wsgi_application()
    application = DjangoWhiteNoise(application)

- create database ``otree`` through `phpMyAdmin <http://localhost/phpmyadmin>`__ (login is root and password is blank)
- update database in ``settings.py``:

.. code-block:: python

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'otree',
            'USER': 'root',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }

- collect static files in one folder: ``python manage.py collectstatic``
- reset database: ``otree resetdb``

Set enviromental variables
~~~~~~~~~~~~~~~~~~~~~~~~~~

- to prepare oTree for real session you need to update the script ``C:\wamp\www\oTree\wsgi.py``:

.. code-block:: python

    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    os.environ['OTREE_PRODUCTION'] = "1"
    os.environ['OTREE_AUTH_LEVEL'] = "STUDY"

    from django.core.wsgi import get_wsgi_application
    from whitenoise.django import DjangoWhiteNoise

    application = get_wsgi_application()
    application = DjangoWhiteNoise(application)
