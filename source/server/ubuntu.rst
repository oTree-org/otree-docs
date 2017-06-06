.. _server-ubuntu:

Linux Server
============

.. note::

    If you are just testing your app locally, you can use
    ``otree runserver``, which is simpler than the below steps.

We typically recommend oTree users to deploy to Heroku (see instructions :ref:`here <heroku>`),
because that is the simplest for people who are not experienced with web server administration.

You can also use your own personal Windows computer as a temporary server.
See :ref:`here <server-windows>`.

However, you may prefer to run oTree on a proper Linux server. Reasons may include:

-   You will be launching your experiment in a setting where internet
    connectivity is lacking
-   You do not want your server to be accessed from the internet
-   You want full control over how your server is configured
-   You want better performance (local servers have less latency)

The below instructions are for Ubuntu 16.04.

.. note::

    There is now a :ref:`Docker-based oTree installation <server-docker>`,
    which may be easier than the below steps.

    Another alternative is to use the VirtualBox Fedora oTree server created by
    Gregory Huber at Yale. You can download it
    `here <https://yale.app.box.com/v/VirtualBoxFedoraOtreeServer>`__,
    or follow the below instructions to configure your own server.

Install apt-get packages
------------------------

Run::

    sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib redis-server git

Create a virtualenv
-------------------

It's a best practice to use a virtualenv::

    python3 -m venv venv_otree

Then in your ``.bashrc`` or ``.bash_profile``, add this command so your venv
is activated each time you start your shell::

    source ~/venv_otree/bin/activate

(Substitute the correct location of your ``venv_otree/`` dir above.)


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

If you get an error that says "password authentication failed for user"
when you run ``otree resetdb`` later,
you may need to edit your ``hba_auth.conf`` to enable password-based authentication.

Install Redis
-------------

If you installed ``redis-server`` through ``apt-get`` as instructed earlier,
Redis should be running on port 6379. You can test with ``redis-cli ping``,
which should output ``PONG``.

If there was an installation problem, you can try installing Redis from an alternate source,
e.g. `here <https://launchpad.net/~chris-lea/+archive/ubuntu/redis-server>`__.

Push your code to the server
----------------------------

You can get your code on the server using SCP, SFTP, Dropbox, etc.
If you are interested in using Git (which is somewhat more advanced),
see the instructions :ref:`here <git-generic>`.

For this tutorial, we will assume you are storing your files under
``/home/my_username/oTree``.

Reset the database on the server
--------------------------------

On the server, ``cd`` to the directory containing your oTree project.
Install the requirements and reset the database::

    pip3 install -r requirements.txt
    otree resetdb


.. _runprodserver:

Running the server
------------------

If you are just testing your app locally, you can use the usual ``runserver``
command.

However, when you want to use oTree in production, you need to run the
production server, which can handle more traffic.

Note: oTree does not run with typical Django WSGI servers like ``gunicorn``,
because it is ASGI based.

Testing the production server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

From your project folder, run::

    otree runprodserver --port=8000

Then navigate in your browser to your server's
IP/hostname followed by ``:8000``.

If you're not using a reverse proxy like Nginx or Apache,
you probably want to run oTree directly on port 80.
This requires superuser permission, so let's use sudo,
but add some extra args to preserve environment variables like ``PATH``,
``DATABASE_URL``, etc::

    sudo -E env "PATH=$PATH" otree runprodserver --port=80

Try again to open your browser;
this time, you don't need to append :80 to the URL, because that is the default HTTP port.

Notes:

-   unlike ``runserver``, ``runprodserver`` does not restart automatically
    when your files are changed.
-   ``runprodserver`` automatically runs Django's ``collectstatic``
    to collect your files under ``_static_root/``.
    If you have already run ``collectstatic``, you can skip it with
    ``--no-collectstatic``.

Set remaining environment variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add the following to your ``.bash_profile`` or ``.bashrc``
(substitute your own values)::

    export OTREE_ADMIN_PASSWORD=my_password
    export OTREE_PRODUCTION=0
    export OTREE_AUTH_LEVEL=DEMO

Process control system
~~~~~~~~~~~~~~~~~~~~~~

Once the server is working as described above,
it's a good practice to use
a process control system like Supervisord or Circus.
This will restart your processes in case they crash,
keep it running if you log out, etc.

Circus
``````

To install::

    sudo apt-get install libzmq-dev libevent-dev
    pip3 install circus circus-web

Create a ``circus.ini`` in your project folder,
with the following content (can do this locally and then git push again)::

    [watcher:webapp]
    cmd = otree
    args = runprodserver --port=80
    use_sockets = True
    copy_env = True

Then run::

    sudo -E env "PATH=$PATH" circusd circus.ini

If this is working properly, you can start it as a daemon::

    sudo -E env "PATH=$PATH" circusd --daemon circus.ini

This command will not produce any output, because all output will be logged
to a file (which file?).

To stop circus, run::

    circusctl quit


Supervisor
``````````
As an alternative to Circus, you can install supervisor::

    sudo apt-get install supervisor

If you install supervisor through apt-get, it will be installed as a service,
and will therefore automatically start when your server boots.
(You can also install supervisor with pip, but unlike oTree it's only compatible
with Python 2, so you should install it into your system's Python 2
installation, rather than your Python 3 virtualenv.)

In the supervisor config dir ``/etc/supervisor/conf.d/``, create a file
``otree.conf`` with the following content::

    [program:otree]
    command=/home/my_username/venv_otree/bin/otree runprodserver --port=80
    directory=/home/my_username/oTree
    stdout_logfile=/home/my_username/otree-supervisor.log
    stderr_logfile=/home/my_username/otree-supervisor-errors.log
    autostart=true
    autorestart=true
    environment=
        PATH="/home/my_username/venv_otree/bin/:%(ENV_PATH)s",
        DATABASE_URL="postgres://otree_user:otree@localhost/django_db",
        OTREE_ADMIN_PASSWORD="my_password", # password for oTree web admin
        OTREE_PRODUCTION="0", # can set to 1
        OTREE_AUTH_LEVEL="", # can set to STUDY or DEMO

``directory`` should be the dir containing your project (i.e. with ``settings.py``).

``DATABASE_URL`` should match what you set earlier. That is, you need to set
``DATABASE_URL`` in 2 places:

-   in your ``.bashrc``, so that ``otree resetdb`` works when you execute
    it as a regular user
-   in your ``otree.conf`` so that ``otree runprodserver`` works
    when it is executed by the root user (normally supervisor runs under the
    root user)

To start or restart the server (e.g. after making changes), do::

    sudo service supervisor restart

If this doesn't start the server, check the ``stdout_logfile`` you defined above,
or ``/var/log/supervisor/supervisord.log``.


(Optional) Apache, Nginx, etc.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can use oTree without Apache or Nginx.
oTree comes installed with the `Daphne <https://github.com/andrewgodwin/daphne>`__ web server,
which is launched automatically when you run ``otree runprodserver``.

oTree does not work with WSGI servers like Gunicorn or mod_wsgi.
Instead it requires an ASGI server, and currently the recommended one is Daphne.
Apache and Nginx do not have ASGI server implementations, so you cannot use
Apache or Nginx as your primary web server.

However, you still might want to use Apache/Nginx as a reverse proxy, for the following reasons:

-   You are trying to optimize serving of static files
    (though oTree uses Whitenoise, which is already fairly efficient)
-   You need to host other websites on the same server
-   You need features like SSL or proxy buffering

Apache
``````
If you want to run oTree on a subdomain of your host so that you can share
port 80 with other sites hosted on the same machine,
you can try the below configuration.
The below example assumes oTree server is running on port 8000.
For HTTPS, change ``80`` to ``443`` ``ws`` prefix to ``wss``::

    <VirtualHost *:80>
            ServerName otree.domain.com
            ProxyRequests Off
            ProxyPreserveHost On
            ProxyPass / http://localhost:8080/
            ProxyPassReverse / http://localhost:8080/

            RewriteEngine On
            RewriteCond %{HTTP:Connection} Upgrade [NC]
            RewriteCond %{HTTP:Upgrade} websocket [NC]
            RewriteRule /(.*) ws://127.0.0.1:8000/$1 [P,L]
    </VirtualHost>



Troubleshooting
---------------

If you get strange behavior,
such as random changes each time the page reloads,
it might be caused by another oTree instance that didn't shut down.
Try stopping oTree and reload again.
Also make sure that you are not sharing the same Postgres or Redis
databases between two oTree instances.


Database backups
----------------

If you are using Postgres, you can export your database to a ``.sql`` file
with a command like this::

    pg_dump -U otree_user -h localhost django_db > otree-$(date +"%Y-%m-%d-%H-%M").sql

(This assumes your database is set up as described above (with username ``otree_user``
and database name ``django_db``, and that you are on Unix.)

If you need to restore your database to a particular backup, do like this::

    psql django_db < otree-2017-03-22-01-01.sql


Sharing a server with other oTree users
---------------------------------------

If multiple oTree users need to share an oTree server
with separate projects, the easiest option might be to use :ref:`Docker <server-docker>`.
See the section at the bottom of the Docker page about sharing the server.
Or, you can follow the below instructions

You can share a server with other oTree users;
you just have to make sure that the code and databases are kept separate,
so they don't conflict with each other.

On the server you should create a different Unix user for each person
using oTree. Then each person should follow the same steps described above,
but in some cases name things differently to avoid clashes:

-   Create a virtualenv in their home directory (can also be named ``venv_otree``)
-   Create a different Postgres database (e.g. ``postgres://otree_user2:mypassword@localhost/django_db``),
    as described earlier,
    and set this in the DATABASE_URL env var.
-   Each user needs their own Redis database.
    By default, oTree uses ``redis://localhost:6379/0``;
    but if another person uses the same server, they need to set the
    ``REDIS_URL`` env var explicitly, to avoid clashes.
    You can set it to ``redis://localhost:6379/1``, ``redis://localhost:6379/2``,
    etc. (which will use databases 1, 2, etc...instead of the default database 0).
    Another option is to run multiple instances of Redis on different ports.
-   Do a ``git init`` in the second user's home directory as described earlier,
    and then add the remote ``my-username2@XXX.XXX.XXX.XXX:oTree.git``
    (assuming their username is ``my-username2``).

Once these steps are done, the second user can git push code to the server,
then run ``otree resetdb``.

If you don't need multiple people to run experiments simultaneously,
then each user can take turns running the server on port 80 with ``otree runprodserver --port=80``.
However, if multiple people need to run experiments at the same time,
then you would need to run the server on different ports, e.g. ``--port=8000``,
``--port=8001``, etc.

Finally, if you use supervisor (or circus) as described above,
each user should have their own conf file, with their personal
parameters like virtualenv path, oTree project path,
``DATABASE_URL`` and ``REDIS_URL`` env vars, port number, etc.

Next steps
----------

See :ref:`server_final_steps` for steps you should take before launching your study.
