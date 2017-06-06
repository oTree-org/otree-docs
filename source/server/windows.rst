.. _server-windows:

Windows Server
==============

If you are just testing your app on your personal computer, you can use
``otree runserver``. You don't need a full server setup as described below,
which is necessary for sharing your app with an audience.

Configure your PC to be a server
--------------------------------

Let's say you have developed your app on your personal computer.
If you only need computers on the same local network to access it
(e.g. your university department network) and don't need to be on the public internet,
you can follow the below steps.

Create a firewall rule
~~~~~~~~~~~~~~~~~~~~~~

You need to allow other computers to connect to oTree through your firewall.

-   Open the Windows Firewall
-   Go to "Inbound Rules"
-   Click "New Rule"
-   Select "Port" to make a port rule
-   Under "Specific local ports", enter 80 and 8000
-   Select "Allow the connection"
-   Click through the next few screens, keeping the defaults
-   Choose a name for your rule (e.g. "oTree").

(If you use Skype) fix Skype issue
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Skype sometimes uses port 80, which can conflict with oTree.
Either quit Skype, or if you need to keep it running,
go in Skype to Tools > Options > Advanced > Connections
and unselect "Use port 80 and 443 for additional incoming connections".

Find your IP address
~~~~~~~~~~~~~~~~~~~~

Open PowerShell or CMD and enter ``ipconfig``.
Look for the entry ``IPv4 Address``.
Maybe it will look something like ``10.0.1.3``, or could also start with 172 or 192.

Run the server
~~~~~~~~~~~~~~

Start the server with your IP address followed by :80, e.g.
``otree runserver 10.0.1.3:80``.

Enter this IP address into the browser of another device on the same network and
you should be able to load the oTree demo page.

If it doesn't work, maybe another app is using port 80 already.

Try starting the server on port 8000 instead of 80.
and then on the client device's browser, connect to the IP address followed by ``:8000``,
e.g. ``10.0.1.3:8000``.


.. _postgres-windows:

Database (Postgres)
-------------------

oTree's default database is SQLite, which is fine for local development,
but insufficient for production.
We recommend PostgreSQL, although you can also use MySQL, MariaDB, or any other database
supported by Django.

Install `Postgres for Windows <http://www.enterprisedb.com/products-services-training/pgdownload#windows>`__,
using the default options. Note down the password you chose for the root ``postgres`` user.

When the installer finishes, open PowerShell and run ``psql -U postgres -W``.
(If the command is not found, make sure your ``PATH`` environment variable contains
``C:\Program Files\PostgreSQL\9.6\bin``.)

Then enter these commands::

    CREATE DATABASE django_db;
    CREATE USER otree_user WITH PASSWORD 'mypassword';
    GRANT ALL PRIVILEGES ON DATABASE django_db TO otree_user;

Then exit the SQL prompt::

    \q

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
your ``DATABASE_URL`` would look like this::

    postgres://otree_user:mypassword@localhost/django_db

To set the environment variable, do a Windows search (or control panel search)
for "environment variables". This will take you to the dialog with a name like
"Edit system environment variables". Add a new system entry for ``DATABASE_URL`` with the above URL.

Then restart PowerShell so the environment variable gets loaded.

Once ``DATABASE_URL`` is defined, oTree will use it instead of the default SQLite.
(This is done via `dj_database_url <https://pypi.python.org/pypi/dj-database-url>`__.)

psycopg2
~~~~~~~~

To use Postgres, you need to install psycopg2 with ``pip3 install psycopg2``.
If the pip install doesn't work,
download it `here <http://www.stickpeople.com/projects/python/win-psycopg/>`__.
(If you are using a virtualenv, note the special installation instructions on that page.)

resetdb
~~~~~~~

If all the above steps went well, you should be able to run ``otree resetdb``.

Install Redis
-------------

You should download and run `Redis for Windows <https://github.com/MSOpenTech/redis/releases>`__.

Redis should be running on port 6379. You can test with ``redis-cli ping``,
which should output ``PONG``.

Next steps
----------

Run the server as described :ref:`here <runprodserver>` the steps are essentially the same as on Linux.

See :ref:`server_final_steps` for steps you should take before launching your study.

Advanced
--------

(Optional) create a virtualenv
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It's a best practice to use a virtualenv (though optional)::

    python3 -m venv venv_otree

You can configure PowerShell to always activate this virtualenv.
Enter::

    notepad $shell

Then put this in the file::

    cd "C:\path\to\oTree"
    . "C:\path\to\oTree\venv_otree\Scripts\activate.ps1"

(Note the dot at the beginning of the line.)


(Optional) use git
~~~~~~~~~~~~~~~~~~

The remaining steps are to deploy your code with Git as described :ref:`here <git-generic>`,
