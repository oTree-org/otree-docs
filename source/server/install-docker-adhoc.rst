.. _install-docker-adhoc:

Docker on your own computer
===========================

You can use Docker to run a virtualized oTree
on your Linux, Windows, or Mac server.
It's like a virtual machine that already has Postgres, Redis, oTree, and Python
configured.
This may be an easy option for people who want to install oTree on their
own servers.

Below are the steps to use Docker.


On your local computer's command line, go to your project folder and run these commands to download
the 4 Docker files (should add them to the same folder as ``requirements.txt``).

If developing on Windows::

    iwr https://raw.githubusercontent.com/oTree-org/otree-docker/master/Dockerfile -OutFile Dockerfile
    iwr https://raw.githubusercontent.com/oTree-org/otree-docker/master/entrypoint.sh -OutFile entrypoint.sh
    iwr https://raw.githubusercontent.com/oTree-org/otree-docker/master/pg_ping.py -OutFile pg_ping.py
    iwr https://raw.githubusercontent.com/oTree-org/otree-docker/master/.dockerignore -OutFile .dockerignore
    iwr https://raw.githubusercontent.com/oTree-org/otree-docker/master/docker-compose-adhoc.yaml -OutFile docker-compose.yaml
    iwr https://raw.githubusercontent.com/oTree-org/otree-docker/master/.env -OutFile .env

If developing on Mac/Linux::

    curl https://raw.githubusercontent.com/oTree-org/otree-docker/master/Dockerfile > Dockerfile
    curl https://raw.githubusercontent.com/oTree-org/otree-docker/master/entrypoint.sh > entrypoint.sh
    curl https://raw.githubusercontent.com/oTree-org/otree-docker/master/pg_ping.py > pg_ping.py
    curl https://raw.githubusercontent.com/oTree-org/otree-docker/master/.dockerignore > .dockerignore
    curl https://raw.githubusercontent.com/oTree-org/otree-docker/master/docker-compose-adhoc.yaml > docker-compose.yaml
    curl https://raw.githubusercontent.com/oTree-org/otree-docker/master/.env > .env

Install Docker
--------------

- Windows: download & run the `installer <https://download.docker.com/win/stable/InstallDocker.msi>`__.
- Log out
- Start docker (make it auto-start as a service?)
- Change settings, reduce memory to 1024. Go to "Advanced".
- You may need to close some programs like PyCharm, Firefox, Chrome, to free up RAM.


Build & run image
-----------------
::

    docker build -t otree .

Run this command, which will install all dependencies
(Python, oTree, Postgres, Redis), reset the DB, and run the production server::

    docker-compose up

This command will start the server and collect static files.
Once it's run,

If you modify your database models and build a new image,
you will need to reset the database.
With Docker, instead of "otree resetdb", you should do::

    docker-compose down -v

If you change your ``docker-compose.yaml`` or ``.env``,
you will need to recreate your container::

    docker-compose up --force-recreate

Allow other computers to connect
--------------------------------

Instructions for :ref:`Windows <windows-adhoc>` or :ref:`Mac <mac-adhoc>`.

Set up Docker
-------------

Open ``.env``, and customize it as you wish.
You should decide what ``OTREE_PORT`` to use.
You should use port 80 if you are a superuser,
and especially if your site needs to be accessed from the internet.
Otherwise, you can use a higher port number like 8000, 8001, etc.
