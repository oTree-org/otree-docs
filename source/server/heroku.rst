.. _heroku:

Basic Server Setup (Heroku)
===========================

`Heroku <https://www.heroku.com/>`__ is a commercial cloud hosting provider.
If you are not experienced with web server administration, Heroku may be
the simplest option for you.

The Heroku free plan is sufficient for small-scale testing of your app,
but once you are ready to launch a study, you should upgrade to a paid server,
which can handle more traffic.

Basic Heroku setup
------------------

Create an account
~~~~~~~~~~~~~~~~~

Create an account on `Heroku <https://www.heroku.com/>`__.
Select Python as your main language. However,
you can
skip the "Getting Started With Python" guide.

Install the Heroku Toolbelt
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install the `Heroku Toolbelt <https://toolbelt.heroku.com/>`__.

This provides you access to the Heroku Command Line utility.

Once installed open PowerShell (Windows) or Terminal (Mac),
and go to your project folder.

Log in using the email address and password you used when
creating your Heroku account:

.. code-block:: bash

    $ heroku login

If the ``heroku`` command is not found,
close and reopen your command prompt.

Initialize your Git repo
~~~~~~~~~~~~~~~~~~~~~~~~

If you haven't already initialized a git repository
run this command from your project's root directory:

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

.. _redis:

Install Redis add-on (new for v0.5+)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You need to install Heroku's `Redis add-on <https://elements.heroku.com/addons/heroku-redis>`__.

This step is required, starting with oTree 0.5.
If you don't do it, you will see an "Application Error":

.. image:: ../_static/heroku-application-error.png
    :align: center
    :scale: 100 %

If Redis is not set up, you may also see messages in your logs saying "Connection refused",
or an error mentioning port 6379.


Upgrade oTree
~~~~~~~~~~~~~

We recommend you upgrade to the latest version of oTree, to get the latest bugfixes.
Run:

.. code-block:: bash

    $ pip3 install -U otree-core

.. note::

.. _requirements_base.txt:

Save to requirements_base.txt
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The above command will just upgrade ``otree-core`` locally.
It will not affect what version is installed on your server.

You need to create a list of all the Python modules you have installed
(including ``otree-core``), and save it to the file in your project's root directory
called ``requirements_base.txt``. Heroku will read this file and install the
same version of each library on your server.

If using Windows PowerShell, enter::

    pip3 freeze | out-file -enc ascii requirements_base.txt

Otherwise, enter::

    pip3 freeze > requirements_base.txt

(Open the file ``requirements_base.txt`` and have a look,
especially for the line that says ``otree-core=x.x.x``
This is the version that will be installed on your server.)

Push your code to Heroku
~~~~~~~~~~~~~~~~~~~~~~~~

Commit your changes (note the dot in ``git add .``):

.. code-block:: bash

    git add .
    git commit -am "your commit message"

Transfer (push) the local repository to Heroku:

.. code-block:: bash

    $ git push heroku master

.. note::

    If you get a message ``push rejected``
    and the error message says ``could not satisfy requirement``,
    open ``requirements_base.txt`` and delete every line except
    the ones for ``Django`` and ``otree-core``.
    The line for Django should say ``Django==1.8.8``.

Reset the oTree database on Heroku.
You can get your app's name by typing ``heroku apps``.

.. code-block:: bash

    $ heroku run otree resetdb

.. note::

    Some users have reported ``django.db.utils.ProgrammingError: table "APP_subsession" does not exist``.
    If this happens to you, please upgrade ``otree-core`` (and remember to update it in your ``requirements_base.txt``).

Open the site in your browser:

.. code-block:: bash

    $ heroku open

(This command must be executed from the directory that contains your project.)

That's it! You should be able to play your app online.
If not, see the next section.

.. _heroku-troubleshooting:

Troubleshooting
~~~~~~~~~~~~~~~

If your app fails to load, e.g. "application error", try the following:

-   Use the command ``heroku logs`` to check the server logs for any error messages
    (or, better yet, enable :ref:`Papertrail <papertrail>`, which provides a nice UI for browsing logs).
-   Make sure you remembered to enable the Heroku Redis add-on (see :ref:`here <redis>`).
-   Run ``heroku run otree --version`` to check that you are using the latest version of otree-core on Heroku.

Making updates and modifications
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When you make modifications to your app and want to push the updates
to Heroku, enter::

    git add .
    git commit -am "my commit message"
    git push heroku master
    # next command only required if you added/removed a field in models.py
    heroku run otree resetdb

You should also regularly update your :ref:`requirements_base.txt <requirements_base.txt>`.

Further steps with Heroku
-------------------------

Below are the steps you should take before launching a real study,
or to further configure your server's behavior.

Look at your server check
~~~~~~~~~~~~~~~~~~~~~~~~~

This is new in oTree 0.5. In the oTree admin interface, click "Server Check" in the header bar.
It will tell you what steps below you need to take.


Turn on timeout worker Dyno (new for v0.5+)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To enable full functionality, you should go to the `Heroku Dashboard <https://dashboard.heroku.com/apps>`__,
click on your app, click to edit the dynos, and turn on the ``timeoutworker``
dyno.

Turning on the second dyno is free, but you may need to register a credit card with Heroku.

If you are just testing your app, oTree will still function without the ``timeoutworker`` dyno,
but if you are running a study with real participants, we recommend turning it on.
This will ensure that the page timeouts defined by ``timeout_seconds``
still work even if a user closes their browser.

If you do not see a ``timeoutworker`` entry, make sure your ``Procfile``
looks like this::

    web: otree webandworkers
    timeoutworker: otree timeoutworker


To add an existing remote:
~~~~~~~~~~~~~~~~~~~~~~~~~~

If you previously created a Heroku app and want to link your local oTree git repository
to that app, use this command:

.. code-block:: bash

    $ heroku git:remote -a [myherokuapp]


Scaling up the server
~~~~~~~~~~~~~~~~~~~~~

The Heroku free plan is sufficient for small-scale testing of your app, but once you are ready to go live,
you need to upgrade to a paid plan.

After you finish your experiment,
you can scale your dynos and database back down,
so then you don't have to pay the full monthly cost.

Postgres (upgrade required)
+++++++++++++++++++++++++++

You need to upgrade your Postgres database to a paid tier
(at least the cheapest paid plan),
because the free version can only store a small amount of data.

To provision the "Hobby Basic" database::

    $ heroku addons:create heroku-postgresql:hobby-basic
    Adding heroku-postgresql:hobby-basic to sushi... done, v69
    Attached as HEROKU_POSTGRESQL_RED
    Database has been created and is available

This command will give you the name of your new DB (in the above example, ``HEROKU_POSTGRESQL_RED``).
Then you need to promote (i.e. "activate") this new database::

    $ heroku pg:promote HEROKU_POSTGRESQL_RED
    Promoting HEROKU_POSTGRESQL_RED_URL to DATABASE_URL... done

More info on the database plans `here <https://elements.heroku.com/addons/heroku-postgresql>`__,
and more technical documentation `here <https://devcenter.heroku.com/articles/heroku-postgresql>`__.

After purchasing the upgraded Postgres, it's recommended to delete the hobby-dev
(free) database, to avoid accidentally using the wrong database.


Upgrade dynos
+++++++++++++

In the Heroku dashboard, click on your app's "Resources" tab,
and in the "dynos" section, select "Upgrade to Hobby".
Then select either "Hobby" or "Professional".

Upgrade Redis (optional)
++++++++++++++++++++++++

I have not seen any problems yet with the free version of Redis.
However, if running a study, consider upgrading to the "Premium 0" Redis for $15/month,
because it features "high availability", which might make your app run more
reliably.

Setting environment variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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


Before launching a study, you should set up Sentry.

.. _sentry:

Logging with Sentry
-------------------

Whether or not you use Heroku,
you should enter your email address (`here <https://docs.google.com/forms/d/1aro9cL4smi1jbyFM--CqsJpr2oRHjNCE-UVHZEYHQcE/viewform>`__)
to sign up for our free Sentry service
which can log all errors on your server and send you email notifications.
(`Sentry <https://getsentry.com/welcome/>`__.)

Sentry is necessary because many errors are not visible in the UI after you turn off debug mode.
You will no longer see Django's yellow error pages; you or your users will just see generic "500 server error" pages.

After you enter your email, you will receive an email with a SENTRY_DSN,
which is a URL you paste into your settings.py.

.. _papertrail:

Logging with Papertrail
-----------------------

If using Heroku, we recommend installing the free "Papertrail" logging add-on::

    heroku addons:create papertrail:choklad

Papertrail gives you an easy-to-use interface for exploring the Heroku server logs.
It is much easier to use than running ``heroku logs``.

(This is useful even if you are already using Sentry, because it shows different types of errors.)

Database backups
----------------

When running studies, it is your responsibility to back up your database.

In Heroku, you can set backups for your Postgres database. Go to your `Heroku Dashboard <https://dashboard.heroku.com/apps/>`__,
click on the "Heroku Postgres" tab, and then click "PG Backups".
More information is available `here <https://devcenter.heroku.com/articles/heroku-postgres-backups>`__.

Modifying an existing database
------------------------------

.. note::

    This section is more advanced and is for people who are comfortable with troubleshooting.

If your database already contains data and you want to update the structure
without running ``resetdb`` (which will delete existing data), you can use Django's migrations feature.
Below is a quick summary; for full info see the Django docs `here <https://docs.djangoproject.com/en/1.9/topics/migrations/#workflow>`__.

The first step is to run ``python manage.py makemigrations my_app_name`` (substituting your app's name),
for each app you are working on. This will create a ``migrations`` directory in your app,
which you should add to your git repo, commit, and push to your server.

Instead of using ``otree resetdb`` on the server, run ``python manage.py migrate`` (or ``otree migrate``).
If using Heroku, you would do ``heroku run otree migrate``.
This will update your database tables.

If you get an error ``NameError: name 'Currency' is not defined``,
you need to find the offending file in your app's ``migrations`` folder,
and add ``from otree.common import Currency`` at the top of the file.

If you make further modifications to your apps, you can run
``python manage.py makemigrations``. You don't need to specify the app names in this command;
migrations will be updated for every app that has a ``migrations`` directory.
Then commit, push, and run ``python manage.py migrate`` again as described above.

More info `here <https://docs.djangoproject.com/en/1.9/topics/migrations/#workflow>`__