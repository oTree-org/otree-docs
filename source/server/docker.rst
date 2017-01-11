.. _server-docker:

Docker
======

You can use Docker to run a virtualized oTree
on your Linux, Windows, or Mac server.
It's like a virtual machine that already has Postgres, Redis, oTree, and Python
configured.
This may be the easiest option for people who want to install oTree on their
own servers.

Below are the steps to use Docker.

.. note::

    These instructions are new, so please send feedback to chris@otree.org.


GitHub
------

(Skip this step if you already have a GitHub repo.)

Create a `GitHub <https://github.com/>`__ account,
then create a repository for your project.
Leave the box unchecked for "Initialize this repository with a README".
After creating the repository, follow the instructions on the next page
to push your code to GitHub.

Docker Hub
----------

-   Go to `Docker Hub <https://hub.docker.com/>`__ and create an account.
-   Follow `these instructions <https://hub.docker.com/>`__
    to create an automated build.
    In summary: in your account settings, go to "Linked Accounts & Services",
    and link your GitHub account.
    Then create an automated build for your GitHub repo.

Add Docker files and push to GitHub
-----------------------------------

Unzip `this file <https://github.com/oTree-org/otree-docker/archive/master.zip>`__.

Put the following files
into your oTree project directory (next to requirements.txt):

-   .dockerignore
-   Dockerfile
-   entrypoint.sh
-   pg_ping.py


Then run::

    git add .
    git commit -am "added docker files"
    git push origin master

Go to Docker Hub and ensure that the automatic build you set up was triggered.


Set up Docker on your server
----------------------------

Docker config files
~~~~~~~~~~~~~~~~~~~

In the folder you unzipped in the previous section,
open ``docker-compose.yaml`` and change the line ``image: otree``
to your Docker Hub user-name/repository-name, e.g.::

    image: YourDockerUsername/oTree

Also, open ``.env`` and customize it as you wish.
You should decide what ``OTREE_PORT`` to use.
You should use port 80 if you are a superuser,
and especially if your site needs to be accessed from outside the network
firewall. Otherwise, you can use a higher port number like 8000, 8001, etc.

Then, login to your server, and create a folder to hold your docker files::

    mkdir otree-docker

Move ``.env`` and ``docker-compose.yaml`` into this folder,
either by SFTP or by copying the file and doing ``cat >docker-compose.yaml``
followed by Ctrl+v, Enter, Ctrl+z

Install Docker Compose on the server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On your server, `install Docker Compose <https://docs.docker.com/compose/install/>`__.

Download your image and start
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

From the server command line, login to Docker::

    docker login

On DockerHub, go to your "Build Details" page,
and check the status of your build.
Once it's finished, run::

    docker-compose pull

Finally, ``cd`` to the folder containing ``docker-compose.yaml``
and run this command, which will install all dependencies
(Python, oTree, Postgres, Redis), reset the DB, and run the production server::

    docker-compose up

If you modify your database models and push a new commit
to Docker Hub, you will need to reset the database on your server.
With Docker, instead of "otree resetdb", you should do::

    docker-compose down -v

Sharing a server with other oTree users
---------------------------------------

If multiple users need to share a server,
you should create a different Unix user account for each person
using oTree.

If users need to run experiments simultaneously,
then each user should edit their ``.env`` file to set a
different ``OTREE_PORT``, e.g. 8000, 8001, etc.
Otherwise, every user can set the ``OTREE_PORT`` to 80.

Sentry
------
It's highly recommended to set up :ref:`Sentry <sentry>`,
so that you can monitor errors on the server

Bots
----

Before launching a study, it's advisable to test your apps with bots,
especially browser bots. See the section :ref:`bots`.
