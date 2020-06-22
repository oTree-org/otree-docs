.. _server-windows:

Windows Server (advanced)
=========================

If you are just testing your app on your personal computer, you can use
``otree zipserver`` or ``otree devserver``. You don't need a full server setup as described below,
which is necessary for sharing your app with an audience.

This section is for people who are experienced with setting up web servers.
If you would like an easier and quicker way, we recommend using
:ref:`Heroku <heroku>`.

.. _why-server:

Why do I need to install server software?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

oTree's development setup (using ``zipserver`` with a SQLite database)
is not designed for running actual studies. One known risk is that
if you don't install Postgres, your SQLite database
might lock when multiple users are accessing it simultaneously.

For a short, small study, you might be able to get away with just using
``devserver``,
as long as you set up your IP address as described in :ref:`server-adhoc`
and run ``otree collectstatic``.

However, for reliable results, you should follow the steps below.

Database (Postgres)
-------------------

oTree's default database is SQLite, which is fine for local development,
but insufficient for production, because it often locks when it multiple
clients are accessing it.

We recommend you use PostgreSQL.
Install `Postgres for Windows <http://www.enterprisedb.com/products-services-training/pgdownload#windows>`__,
using the default options. Note down the password you chose for the root ``postgres`` user.

Launch pgAdmin, and using the browser, create a new database called ``django_db``.
Now, edit your ``pg_hba.conf``, which is usually located in ``C:\Program Files\PostgreSQL\``.
On the lines for ``IPv4`` and ``IPv6``, change the ``METHOD`` from ``md5`` to ``trust``.

Now, set your ``DATABASE_URL`` environment variable to this::

    postgres://postgres@localhost/django_db

Then restart your Command Prompt so the environment variable gets loaded.

Once ``DATABASE_URL`` is defined, oTree will use it instead of the default SQLite.


psycopg2
~~~~~~~~

To use Postgres, you need to install psycopg2 with ``pip3 install psycopg2``.
If the pip install doesn't work,
download it `here <http://www.stickpeople.com/projects/python/win-psycopg/>`__.
(If you are using a virtualenv, note the special installation instructions on that page.)

resetdb
~~~~~~~

If all the above steps went well, you should be able to run ``otree resetdb``.

.. _redis-windows:

Install Redis
-------------

You should download and run `Redis for Windows <https://github.com/MSOpenTech/redis/releases>`__.

Redis should be running on port 6379. You can test with ``redis-cli ping``,
which should output ``PONG``.

Run the production server
-------------------------

Run::

    otree prodserver 80

See :ref:`here <prodserver>` for full instructions.
The steps are essentially the same as on Linux.

Set environment variables
-------------------------

You should set ``OTREE_ADMIN_PASSWORD``, ``OTREE_PRODUCTION``, and ``OTREE_AUTH_LEVEL``.

Allow other computers to connect
--------------------------------

See instructions :ref:`here <server-adhoc>`.
