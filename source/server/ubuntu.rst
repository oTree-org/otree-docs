.. _server-ubuntu:

oTree on Linux (Ubuntu)
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

Python & Pip
------------

We recommmend installing using your system's package manager to install Python 3.5.
If you use the default system Python 2.7 installation,
we recommend running ``pip install --upgrade pip``,
because the default system Python can have an outdated version of Pip.
If ``Twisted`` fails to compile, install the ``python-dev`` package (e.g. through ``apt-get``).

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
allows you to continue to use SQLite on your development machine, while using Postgres on your production server.


Then run::

    pip install -r requirements.txt

Note it is ``requirements.txt``, instead of ``requirements_base.txt``.
This will install some extra packages like ``psycopg2``,
which is necessary for using Postgres.

You may get an error when you try installing ``psycopg2``, as described
`here <http://initd.org/psycopg/docs/faq.html#problems-compiling-and-deploying-psycopg2>`__.

The fix is to install the ``libpq-dev`` and ``python-dev`` packages.
On Ubuntu/Debian, do:

.. code-block:: bash

    sudo apt-get install libpq-dev python-dev


Install Redis
-------------

You need to install Redis server and run it on its default port (6379).

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
launch all server processes (``daphne`` server, Channels worker processes,
and the timeout worker).

.. warning::

    Prior to v0.5, oTree used ``gunicorn``.
    oTree 0.5 and later uses the ``daphne`` server.

.. note::

    Prior to otree-core 0.5.16, ``runprodserver`` executed the commands in your ``Procfile``.
    It no longer does so.

Next steps
----------

Set up :ref:`Sentry <sentry>`.
