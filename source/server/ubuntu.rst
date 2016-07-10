.. _server-ubuntu:

Linux Server
============

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

The below instructions are for Ubuntu 16.04.

.. note::

    Prof. Gregory Huber at Yale has created a VirtualBox Fedora image with oTree server configured.
    You can download it `here <https://yale.app.box.com/v/VirtualBoxFedoraOtreeServer>`__,
    or follow the below instructions to configure your own server.

Install apt-get packages
------------------------

Run::

    sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib redis-server

Create a virtualenv
-------------------

It's a best practice to use a virtualenv::

    python3 -m venv venv_otree

Then in your ``.bashrc`` or ``.bash_profile``, add this command so your venv
is activated each time you start your shell::

    source ~/path/to/your/venv_otree/bin/activate


.. _postgres-linux:

Database (Postgres)
-------------------

oTree's default database is SQLite, which is fine for local development,
but insufficient for production.
We recommend PostgreSQL, although you can also use MySQL, MariaDB, or any other database
supported by Django.

Change users to the ``postgres`` user, so that you can execute some commands::

    sudo su - postgres

Then start the Postgres shell::

    psql

Once you're in the shell, create a database and user::

    CREATE DATABASE django_db;
    CREATE USER otree_user WITH PASSWORD 'mypassword';
    GRANT ALL PRIVILEGES ON DATABASE django_db TO otree_user;

Exit the SQL prompt::

    \q

Exit out of the postgres user and return to your regular command prompt::

    exit

Now you should tell oTree to use Postgres instead of SQLite.
The default database configuration in ``settings.py`` is::

    DATABASES = {
        'default': dj_database_url.config(
            default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
        )
    }

However, instead of modifying the above line directly,
it's better to set the ``DATABASE_URL`` environment variable on your server.
Setting the database through an environment variable
allows you to continue to use SQLite on your development machine,
while using Postgres on your production server.

If you used the values in the example above (username ``otree_user``, password ``mypassword`` and database ``django_db``),
you would add this line to your ``.bash_profile`` or ``.bashrc``::

    export DATABASE_URL=postgres://otree_user:mypassword@localhost/django_db

Then restart your shell, and confirm the env var is set, with ``echo $DATABASE_URL``.
Once ``DATABASE_URL`` is defined, oTree will use it instead of the default SQLite.
(This is done via `dj_database_url <https://pypi.python.org/pypi/dj-database-url>`__.)

Then run::

    pip3 install psycopg2
    otree resetdb

Install Redis
-------------

If you installed ``redis-server`` through ``apt-get`` as instructed earlier,
Redis should be running on port 6379. You can test with ``redis-cli ping``,
which should output ``PONG``.

If there was an installation problem, you can try installing Redis from an alternate source,
e.g. `here <https://launchpad.net/~chris-lea/+archive/ubuntu/redis-server>`__.

.. _git-generic:

Deploy your code
----------------

If your code is on your personal computer and you are trying to push it to
this web server, you can use Git.

Open your shell, and make sure you have committed any changes as follows:

.. code-block:: bash

    pip3 freeze > requirements_base.txt
    git add .
    git commit -am '[commit message]'

(If you get the message
``fatal: Not a git repository (or any of the parent directories): .git``
then you first need to initialize the git repo.)

Then do:

.. code-block:: bash

    $ git push [remote name] master

Where [remote name] is the name of your server's git remote.

.. _runprodserver:

Running the server
------------------

If you are just testing your app locally, you can use the usual ``runserver``
command.

However, when you want to use oTree in production, you need to run the
production server, which can handle more traffic.

.. note::

    Prior to v0.5, oTree used ``gunicorn``.
    oTree 0.5 and later uses the ``daphne`` server.

.. note::

    Prior to otree-core 0.5.16, ``runprodserver`` executed the commands in your ``Procfile``.
    It no longer does so.

You should use a process control system like `Circus <https://circus.readthedocs.io/en/latest/>`__ or Supervisord,
which will restart your processes in case they crash.
Instructions are given here for Circus,
because it is compatible with Python 3.

Circus
~~~~~~

Install circus::

    sudo apt-get install libzmq-dev libevent-dev
    pip3 install circus circus-web

Create a ``circus.ini`` in your project folder somewhere, with the following content::

    [watcher:webapp]
    cmd = otree
    args = runprodserver --no-collectstatic
    use_sockets = True

The command ``otree runprodserver`` will run
all server processes (``daphne`` server, Channels worker processes,
and the timeout worker).

Run the following commands::

    otree collectstatic
    circusd --daemon circus.ini

Apache, Nginx, etc.
~~~~~~~~~~~~~~~~~~~

It's simplest to use oTree without Apache or Nginx.
oTree comes installed with its own web server `Daphne <https://github.com/andrewgodwin/daphne>`__,
which is launched automatically when you run ``otree runprodserver``.

oTree does not work with WSGI servers like Gunicorn or mod_wsgi.
Instead it requires an ASGI server, and currently the best one is Daphne.
Apache and Nginx do not have ASGI server implementations, so you cannot use
Apache or Nginx as your primary web server.

You could still use Apache/Nginx as a reverse proxy, for example if you are
trying to optimize performance. However, for many people ``daphne`` will be sufficient.
oTree uses `whitenoise <http://whitenoise.evans.io/en/stable/index.html>`__
to serve static files (e.g. images, JavaScript, CSS). This is reasonably
efficient, so for many people a reverse proxy will not be necessary.

Next steps
----------

Set up :ref:`Sentry <sentry>`.

