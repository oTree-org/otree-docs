.. _server-ubuntu:

Ubuntu Linux Server
===================

We typically recommend newcomers to oTree to deploy to Heroku
(see instructions :ref:`here <heroku>`),
or to use their own personal computer as a temporary server (see :ref:`here <server-adhoc>`).

However, you may prefer to run oTree on a proper Linux server. Reasons may include:

-   Your lab doesn't have internet
-   You want full control over server configuration
-   You want better performance (local servers have less latency)

If you are experienced in Django server setup, you just need to know that
setting up an oTree server is the same as any Django project, except:

-   You need Redis
-   You start the server with ``otree runprodserver``, rather than a WSGI server.

Install apt-get packages
------------------------

Run::

    sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib redis-server git

Create a virtualenv
-------------------

It's a best practice to use a virtualenv::

    python3 -m venv venv_otree

To activate this venv every time you start your shell, put this in your ``.bashrc`` or ``.profile``::

    source ~/venv_otree/bin/activate

Once your virtualenv is active, you will see ``(venv_otree)`` at the beginning
of your prompt.

.. _postgres-linux:

Database (Postgres)
-------------------

oTree's default database is SQLite, which is fine for local development,
but insufficient for production.
We recommend you use PostgreSQL.

Change users to the ``postgres`` user, so that you can execute some commands::

    sudo su - postgres

Then start the Postgres shell::

    psql

Once you're in the shell, create a database and user::

    CREATE DATABASE django_db;
    alter user postgres password 'password';

Exit the SQL prompt::

    \q

Return to your regular command prompt::

    exit


Then add this line to the end of your .bashrc/.profile::

    export DATABASE_URL=postgres://postgres:postgres@localhost/django_db

Once ``DATABASE_URL`` is defined, oTree will use it instead of the default SQLite.

When you run ``otree resetdb`` later,
if you get an error that says "password authentication failed for user",
find your ``hba_auth.conf`` file, and on the lines for ``IPv4`` and ``IPv6``,
change the ``METHOD`` from ``md5`` (or whatever it currently is) to ``trust``.

Install Redis
-------------

If you installed ``redis-server`` through ``apt-get`` as instructed earlier,
Redis should be running on port 6379. You can test with ``redis-cli ping``,
which should output ``PONG``.

If there was an installation problem, you can try installing Redis from an alternate source,
e.g. `here <https://launchpad.net/~chris-lea/+archive/ubuntu/redis-server>`__.

Push your code to the server
----------------------------

You can get your code on the server using SCP, SFTP, Git, etc.

For this tutorial, we will assume you are storing your files under
``/home/my_username/oTree``.

Reset the database on the server
--------------------------------

On the server, ``cd`` to the folder containing your oTree project.
Install the requirements and reset the database::

    pip3 install -r requirements.txt
    otree resetdb


.. _runprodserver:

Running the server
------------------

If you are just testing your app locally, you can use the usual ``devserver``
command.

However, when you want to use oTree in production, you need to run the
production server, which can handle more traffic.

Note: oTree does not run with typical Django WSGI servers like ``gunicorn``,
because it is ASGI based.

Testing the production server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

From your project folder, run::

    otree runprodserver 8000

Then navigate in your browser to your server's
IP/hostname followed by ``:8000``.

If you're not using a reverse proxy like Nginx or Apache,
you probably want to run oTree directly on port 80.
This requires superuser permission, so let's use sudo,
but add some extra args to preserve environment variables like ``PATH``,
``DATABASE_URL``, etc::

    sudo -E env "PATH=$PATH" otree runprodserver 80

Try again to open your browser;
this time, you don't need to append :80 to the URL, because that is the default HTTP port.

Notes:

-   unlike ``devserver``, ``runprodserver`` does not restart automatically
    when your files are changed.
-   ``runprodserver`` automatically runs Django's ``collectstatic``
    to collect your files under ``_static_root/``.
    If you have already run ``collectstatic``, you can skip it with
    ``--no-collectstatic``.

Set remaining environment variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add these in the same place where you set ``DATABASE_URL``::

    export OTREE_ADMIN_PASSWORD=my_password
    #export OTREE_PRODUCTION=1 # uncomment this line to enable production mode
    export OTREE_AUTH_LEVEL=DEMO

(Optional) Process control system
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once the server is working as described above,
it's a good practice to use
a process control system like Supervisord or Circus.
This will restart your processes in case they crash,
keep it running if you log out, etc.

Circus
``````

Install Circus, then create a ``circus.ini`` in your project folder,
with the following content::

    [watcher:webapp]
    cmd = otree
    args = runprodserver 80
    use_sockets = True
    copy_env = True

Then run::

    sudo -E env "PATH=$PATH" circusd circus.ini

If this is working properly, you can start it as a daemon::

    sudo -E env "PATH=$PATH" circusd --daemon circus.ini --log-output=circus-logs.txt


To stop circus, run::

    circusctl stop

(Optional) Apache, Nginx, etc.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You cannot use Apache or Nginx as your primary web server,
because oTree must be run with an ASGI server.
However, you still might want to use Apache/Nginx as a reverse proxy, for the following reasons:

-   You are trying to optimize serving of static files
    (though oTree uses Whitenoise, which is already fairly efficient)
-   You need to host other websites on the same server
-   You need features like SSL or proxy buffering

Troubleshooting
---------------

If you get strange behavior,
such as random changes each time the page reloads,
it might be caused by another oTree instance that didn't shut down.
Try stopping oTree and reload again.
Also make sure that you are not sharing the same Postgres or Redis
databases between two oTree instances.

Sharing a server with other oTree users
---------------------------------------

You can share a server with other oTree users;
you just have to make sure that the code and databases are kept separate,
so they don't conflict with each other.

On the server you should create a different Unix user for each person
using oTree. Then each person should follow the same steps described above,
but in some cases name things differently to avoid clashes:

-   Create a virtualenv in their home directory (can also be named ``venv_otree``)
-   Create a different Postgres database (e.g. ``postgres://otree_user2:mydbpassword@localhost/django_db``),
    as described earlier,
    and set this in the DATABASE_URL env var.
-   Each user needs their own Redis database.
    By default, oTree uses ``redis://localhost:6379``;
    but if another person uses the same server, they need to set the
    ``REDIS_URL`` env var explicitly, to avoid clashes.
    You can set it to ``redis://localhost:6379/1``, ``redis://localhost:6379/2``,
    etc. (which will use databases 1, 2, etc...instead of the default database 0).
    Another option is to run multiple instances of Redis on different ports.

Once these steps are done, the second user can push code to the server,
then run ``otree resetdb``.

If you don't need multiple people to run experiments simultaneously,
then each user can take turns running the server on port 80 with ``otree runprodserver 80``.
However, if multiple people need to run experiments at the same time,
then you would need to run the server on multiple ports, e.g. ``8000``,
``8001``, etc.

Finally, if you use supervisor (or circus) as described above,
each user should have their own conf file, with their personal
parameters like virtualenv path, oTree project path,
``DATABASE_URL`` and ``REDIS_URL`` env vars, port number, etc.

Next steps
----------

See :ref:`server_final_steps` for steps you should take before launching your study.
