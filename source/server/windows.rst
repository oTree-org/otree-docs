.. _server-windows:

Windows Server
==============

If you are just testing your app on your personal computer, you can use
``otree runserver``. You don't need a full server setup as described below,
which is necessary for sharing your app with an audience.

Before deploying to a Windows server, you should consider
using :ref:`Heroku <heroku>` or :ref:`Linux <server-ubuntu>`,
which are more tested.

Create a virtualenv
-------------------

It's a best practice to use a virtualenv (though optional)::

    python3 -m venv venv_otree

You can configure PowerShell to always activate this virtualenv.
Enter::

    notepad $shell

Then put this in the file::

    cd "C:\path\to\oTree"
    . "C:\path\to\oTree\venv_otree\Scripts\activate.ps1"

(Note the dot at the beginning of the line.)

.. _postgres-windows:

Database (Postgres)
-------------------

oTree's default database is SQLite, which is fine for local development,
but insufficient for production.
We recommend PostgreSQL, although you can also use MySQL, MariaDB, or any other database
supported by Django.

Install `Postgres for Windows <http://www.enterprisedb.com/products-services-training/pgdownload#windows>`__,
using the default options. Note down the password you chose for the root ``postgres`` user.

When the installer finishes, open PowerShell and run ``psql -U postgres``.
(If the command is not found, make sure your ``PATH`` environment variable contains
``C:\Program Files\PostgreSQL\9.5\bin``.)

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

You then need to install psycopg2, the Postgres driver for Python.
Installing it via pip often doesn't work. Instead, download it `here <http://www.stickpeople.com/projects/python/win-psycopg/>`__.
If you are using a virtualenv, note the special installation instructions on that page.

If you are using a version of Python prior to 3.5.2,
the installer may report that Python was not found in the registry.
To fix this, upgrade to Python 3.5.2+. If that is not possible,
there is a trick that involves editing the registry. Open ``regedit.exe``,
go to ``HKEY_CURRENT_USER\SOFTWARE\Python\PythonCore\``, and rename 3.5.x to 3.5.

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

The remaining steps are to deploy your code with Git as described :ref:`here <git-generic>`,
and run the server as described :ref:`here <runprodserver>` the steps are essentially the same as on Linux.

Then set up :ref:`Sentry <sentry>`.
