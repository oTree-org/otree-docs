Server deployment
=================

You can develop and test your app locally on your personal computer,
using the ordinary ``runserver`` command.

However, when you want to share your app with an audience,
you must deploy to a web server. oTree can be deployed to a cloud service like
Heroku, or to your own on-premises server.

Heroku
------

`Heroku <https://www.heroku.com/>`__ is a commercial cloud hosting provider.
If you are not experienced with web server administration, Heroku may be
the simplest option for you.

The Heroku free plan is sufficient for small-scale testing of your app,
but once you are ready to go live, you should upgrade to a paid server,
which can handle more traffic.

Here are the steps for deploying to Heroku.

Create an account
~~~~~~~~~~~~~~~~~

Create an account on `Heroku <https://www.heroku.com/>`__. You can
skip the "Getting Started With Python" guide.

Install the Heroku Toolbelt
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install the `Heroku Toolbelt <https://toolbelt.heroku.com/>`__.

This provides you access to the Heroku Command Line utility.

Once installed, you can use the ``heroku`` command from PowerShell (Windows) or Terminal (Mac). (If using the oTree launcher, click the "terminal" button.)

Log in using the email address and password you used when
creating your Heroku account:

.. code-block:: bash

    $ heroku login

Initialize your Git repo
~~~~~~~~~~~~~~~~~~~~~~~~

If you haven't already initialized a git repository, run:

.. code-block:: bash

    git init


Create the Heroku app
~~~~~~~~~~~~~~~~~~~~~

Create an app on Heroku, which prepares Heroku to receive your source
code:

.. code-block:: bash

    $ heroku create
    Creating lit-bastion-5032 in organization heroku... done, stack is cedar-14
    http://lit-bastion-5032.herokuapp.com/ | https://git.heroku.com/lit-bastion-5032.git
    Git remote heroku added
    When you create an app, a git remote (called heroku) is also created and associated with your local git repository.

Heroku generates a random name (in this case lit-bastion-5032) for your
app. Or you can specify your own name; see ``heroku help create`` for more info.
(And see ``heroku help`` for general help.)


Upgrade oTree
~~~~~~~~~~~~~

We recommend you use the latest version of oTree, to get the latest bugfixes.
Run:

.. code-block:: bash

    $ pip install --upgrade otree-core

Deploy your code
~~~~~~~~~~~~~~~~

Commit your changes:

.. code-block:: bash

    pip freeze > requirements_base.txt
    git add .
    git commit -am "[commit message]"

Transfer (push) the local repository to Heroku:

.. code-block:: bash

    $ git push heroku master

Reset the oTree database on Heroku.

.. code-block:: bash

    $ otree-heroku resetdb [your heroku app name]

.. note::

    If you get the error ``TypeError: can only concatenate list (not "tuple") to list``,
    you should upgrade otree-core to the latest version (see :ref:`upgrade-otree-core`)

Open the site in your browser:

.. code-block:: bash

    $ heroku open

(This command must be executed from the directory that contains your project.)


Turn on worker Dyno
~~~~~~~~~~~~~~~~~~~

To enable full functionality, you should go to the `Heroku Dashboard <https://dashboard.heroku.com/apps>`__,
click on your app, click to edit the dynos, and turn on the "worker"
dyno.

.. image:: _static/heroku-worker-dyno.JPG
    :align: center
    :scale: 100 %

You may need to upgrade from Heroku's "free" to "hobby" tier to turn on the
worker dyno.

If you are just testing your app, oTree will still function without the "worker" dyno,
but if you are running a study with real participants, we recommend turning it on.
This will ensure that the page timeouts defined by ``timeout_seconds``
still work even if a user closes their browser.

.. note::

    If you do not see a "worker" entry, make sure your ``Procfile``
    looks like `this <https://github.com/oTree-org/oTree/blob/master/Procfile>`__.


To add an existing remote:
~~~~~~~~~~~~~~~~~~~~~~~~~~

If you previously created a Heroku app and want to link your local oTree git repository
to that app, use this command:

.. code-block:: bash

    $ heroku git:remote -a [myherokuapp]

Scaling up the server
~~~~~~~~~~~~~~~~~~~~~

The Heroku free plan is sufficient for small-scale testing of your app, but once you are ready to go live,
we recommend you upgrade your Postgres database to a paid tier (because the row limit of the free version is very low),
and scale up your dynos to at least the cheapest paid plan. Note: after you finish your experiment,
you can scale your dynos and database back down,
so then you don't have to pay the full monthly cost.

Setting environment variables (optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you would like to turn off debug mode, you should set the ``OTREE_PRODUCTION``
environment variable, like this:

.. code-block:: bash

    $ heroku config:set OTREE_PRODUCTION=1

However, this will hide error pages, so you should set up :ref:`sentry`.

To password protect parts of the admin interface,
you should set ``OTREE_AUTH_LEVEL``):

.. code-block:: bash

    $ heroku config:set OTREE_AUTH_LEVEL=DEMO

More info at :ref:`AUTH_LEVEL`.

Deploying to an on-premises server
----------------------------------

.. note::

    If you are just testing your app locally, you can use the ``resetdb`` and
    ``runserver`` commands, which are simpler than the below steps.

Although Heroku deployment may be the easiest option,
you may prefer to run oTree on your own server. Reasons may include:

-  You do not want your server to be accessed from the internet
-  You will be launching your experiment in a setting where internet
   access is unavailable
-  You want full control over how your server is configured

oTree runs on top of Django, so oTree setup is the same as Django setup.
Django runs on a wide variety of servers, except getting it to run on
a Windows server like IIS may require extra work; you can find info about
Django + IIS online. Below, instructions are given for using Unix and Gunicorn.

Database
~~~~~~~~

oTree is most frequently used with PostgreSQL as the production
database, although you can also use MySQL, MariaDB, or any other database
supported by Django.

You can create your database with a command like this:

.. code-block:: bash

    $ psql -c 'create database django_db;' -U postgres

Then, you should set the following environment variable, so that it can
be read by ``dj_database_url``:

``DATABASE_URL=postgres://postgres@localhost/django_db``

Then, instead of installing ``requirements_base.txt``, install ``requirements.txt``.
This will install ``psycopg2``, which is necessary for using Postgres.

You may get an error when you try installing ``psycopg2``, as described
`here <http://initd.org/psycopg/docs/faq.html#problems-compiling-and-deploying-psycopg2>`__.

The fix is to install the ``libpq-dev`` and ``python-dev`` packages.
On Ubuntu/Debian, do:

.. code-block:: bash

    sudo apt-get install libpq-dev python-dev

The command ``otree resetdb`` only works on SQLite.
On Postgres, you should drop the database and then run ``otree migrate``.

Deploy your code
~~~~~~~~~~~~~~~~

If you are using a remote webserver, you need to push your code there,
typically using Git.

Open your shell (if using the launcher, click the "Terminal" button).

Make sure you have committed any changes as follows:

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
~~~~~~~~~~~~~~~~~~

If you are just testing your app locally, you can use the usual ``runserver``
command.

However, when you want to use oTree in production, you need to run the
production server, which can handle more traffic. You should use a process
control system like Supervisord, and have it launch otree with the command
``otree runprodserver``.

This will run the ``collectstatic`` command, and then
launch the server as specified in the ``Procfile`` in your project's root
directory. The default ``Procfile`` launches the Gunicorn server.
If you want to use another server like Nginx, you need to modify the
``Procfile``. (If you instead want to use Apache, consult the Django docs.)

.. warning::

    Gunicorn doesn't work on Windows, so if you are trying to run oTree on a
    Windows server or use ``runprodserver`` locally on your Windows PC, you
    will need to specify a different server in your ``Procfile``.


.. _sentry:

Sentry
------

We recommend you use our free Sentry service (sign up `here <https://docs.google.com/forms/d/1aro9cL4smi1jbyFM--CqsJpr2oRHjNCE-UVHZEYHQcE/viewform>`__),
which can log all errors on your server and send you email notifications.
(`General info on Sentry <https://getsentry.com/welcome/>`__.)

A service like Sentry is necessary because once you have turned on ``OTREE_PRODUCTION``,
you will no longer see Django's yellow error pages; you or your users will just see generic "500 server error" pages.
Sentry can send you the details of each error by email.

Once you have signed up, we will send you a registration link you need to click.
You will also be provided with a special URL called a "Sentry DSN".

Make sure you have a recent version of oTree-core (0.4.11 or newer).
Then, in your ``settings.py``, you should set ``SENTRY_DSN`` to your DSN URL,
which makes your server send crash info to our Sentry server.
Once that is done, you will automatically get notified with any exceptions when debug mode is turned off.
You can also view the errors through the `web interface <http://sentry.otree.org/auth/login/sentry/>`__.

If you later want other collaborators on your team to receive emails as well, or if you need to manage multiple projects,
send an email to chris@otree.org.