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

.. note::

    Prior to v0.5, oTree used ``gunicorn``.
    oTree 0.5 and later uses the ``daphne`` server.


Supervisor
~~~~~~~~~~

You should use a process control system like Supervisord that runs oTree as a service.
This will start oTree when the machine is booted, restart your processes in case they crash,
keep it running if you log out, etc.

Install supervisor::

    sudo apt-get install supervisor

In the supervisor config dir ``/etc/supervisor/conf.d/``, create a file
``otree.conf`` with the following content::

    [program:otree]
    command=/home/my_username/venv_otree/bin/otree runprodserver --port=80 --no-collectstatic
    directory=/home/my_username/oTree
    stdout_logfile=/home/my_username/otree-supervisor.log
    stderr_logfile=/home/my_username/otree-supervisor-errors.log
    autostart=true
    autorestart=true
    environment=
        PATH="/home/my_username/venv_otree/bin/:%(ENV_PATH)s",
        DATABASE_URL="postgres://otree_user:otree@localhost/django_db",
        OTREE_ADMIN_PASSWORD="my_password",
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

    otree collectstatic
    sudo service supervisor restart


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

Next steps
----------

Set up :ref:`Sentry <sentry>`.

