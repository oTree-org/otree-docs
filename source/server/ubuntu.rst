.. _server-ubuntu:

Linux Server
============

.. note::

    If you are just testing your app locally, you can use
    ``otree runserver``, which is simpler than the below steps.

We typically recommend oTree users to deploy to Heroku (see instructions :ref:`here <heroku>`),
because that is the simplest for people who are not experienced with web server administration.

However, you may prefer to run oTree on your own server. Reasons may include:

-   You will be launching your experiment in a setting where internet
    connectivity is lacking
-   You do not want your server to be accessed from the internet
-   You want full control over how your server is configured
-   You want better performance (local servers have less latency)


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

Set up Git
----------

If your code is on your personal computer and you are trying to push it to
this web server, you can use Git.

On the server
~~~~~~~~~~~~~

On the server, create 2 directories -- one to store your project files,
and another to serve as the Git remote::

    mkdir oTree
    mkdir oTree.git

Create a git repo in ``oTree.git``::

    cd oTree.git
    git init --bare

Using a text editor such as ``nano``, ``emacs``, ``vim``, add the following to
``oTree.git/hooks/post-receive``::

    emacs hooks/post-receive

Then add the following lines to that file::

    #!/bin/sh
    GIT_WORK_TREE=/path/to/your/oTree
    export GIT_WORK_TREE
    git checkout -f

This means that every time someone pushes to ``oTree.git``, the code will be
checked out to the other directory ``oTree``. (This technique is further described
`here <http://toroid.org/git-website-howto>`__.)

Make sure that ``post-receive`` is executable::

    chmod +x hooks/post-receive

On your PC
~~~~~~~~~~

On your PC, open your shell, and make sure you have committed any changes as follows:

.. code-block:: bash

    pip3 freeze > requirements_base.txt
    git add .
    git commit -am '[commit message]'

(If you get the message
``fatal: Not a git repository (or any of the parent directories): .git``
then you first need to initialize the git repo.)

Then add your server as a remote::

    git remote add my-server my-username@XXX.XXX.XXX.XXX:oTree.git

Substitute these values in the above command:
-   ``my-username`` is the Linux login username
-   ``XXX.XXX.XXX.XXX`` is the server's IP address or hostname
-   ``oTree.git`` is the folder with the empty git repo,
-   ``my-server`` is the name you choose to call your remote (e.g. when doing ``git push``).

Then push to this remote::

    $ git push my-server master


Reset the database on the server
--------------------------------

From the directory with your oTree code,
install the requirements and reset the database::

    pip3 install -r requirements.txt
    otree resetdb


.. _runprodserver:

Running the server
------------------

If you are just testing your app locally, you can use the usual ``runserver``
command.

However, when you want to use oTree in production, you need to run the
production server, which can handle more traffic.

Note: oTree does not run with typical Django WSGI servers like ``gunicorn``.
It needs the special ``daphne`` server, which supports WebSockets.


Testing the production server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

From your project folder, run::

    otree runprodserver --port=80

This will run Django's ``collectstatic`` to collect your static files,
then start the server.
If it works, you will be able to navigate in your browser to your server's
IP address or hostname. You don't need to append :80 to the URL,
because that is the default HTTP port.

Note: unlike ``runserver``, ``runprodserver`` does not restart automatically
when your files are changed.

Process control system
~~~~~~~~~~~~~~~~~~~~~~

Once the server is working as described above,
it's a good practice to use
a process control system like Supervisord or Circus.
This will restart your processes in case they crash,
keep it running if you log out, etc.

Supervisor
``````````

Install supervisor::

    sudo apt-get install supervisor

(If you install supervisor through apt-get, it will be installed as a service,
and will therefore automatically start when your server boots.)

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

-   in your ``.bashrc``, so that ``otree resetdb`` works
-   in your ``otree.conf`` so that ``otree runprodserver`` works.

Because normally supervisor executes ``otree runprodserver`` as the root user,
but you execute ``otree resetdb`` as regular (non-root) user.
So the env var needs to be set in both environments.

To start or restart the server (e.g. after making changes), do::

    sudo service supervisor restart


If this doesn't start the server, check the ``stdout_logfile`` you defined above,
or ``/var/log/supervisor/supervisord.log``.

Alternative: Circus
```````````````````

An alternative to Supervisor is `Circus <https://circus.readthedocs.io/en/latest/>`__.

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

Run the following commands::

    otree collectstatic
    circusd circus.ini

If this is working properly, you can start it as a daemon::

    circusd --daemon circus.ini


Apache, Nginx, etc.
~~~~~~~~~~~~~~~~~~~

You can use oTree without Apache or Nginx.
oTree comes installed with the `Daphne <https://github.com/andrewgodwin/daphne>`__ web server,
which is launched automatically when you run ``otree runprodserver``.

oTree does not work with WSGI servers like Gunicorn or mod_wsgi.
Instead it requires an ASGI server, and currently the main/best one is Daphne.
Apache and Nginx do not have ASGI server implementations, so you cannot use
Apache or Nginx as your primary web server.

You could still use Apache/Nginx as a reverse proxy, for example if you are
trying to optimize performance, or if you need features like SSL or proxy buffering.
However, in terms of performance, Daphne alone should be sufficient for many people.
And oTree uses `Whitenoise <http://whitenoise.evans.io/en/stable/index.html>`__
to serve static files (e.g. images, JavaScript, CSS). This is reasonably
efficient, so for many people a reverse proxy will not be necessary.

Sentry
------

It's highly recommended to set up :ref:`Sentry <sentry>`.

Database backups
----------------

If you are using Postgres, you can export your database to a file called ``otree.sql``
with a command like this::

    pg_dump -U otree_user -h localhost django_db > otree-$(date +"%Y-%m-%d-%H-%M").sql

(This assumes your database is set up as described above (with username ``otree_user``
and database name ``django_db``, and that you are on Unix.)

Bots
----

Before launching a study, it's advisable to test your apps with bots,
especially browser bots. See the section :ref:`bots`.

Sharing a server with other oTree users
---------------------------------------

.. note::

    These instructions are preliminary and not fully tested.
    I welcome feedback/revisions.

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
