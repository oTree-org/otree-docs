.. _server-docker:

Docker
======

You can use Docker to run a virtualized oTree
on your Linux, Windows, or Mac server.
It's like a virtual machine that already has Postgres, Redis, oTree, and Python
configured.
This may be an easy option for people who want to install oTree on their
own servers.

Below are the steps to use Docker.

.. note::

    These instructions are new, so please send feedback to chris@otree.org.


GitHub/BitBucket
----------------

(Skip this step if you already have a GitHub repo.)

(Note: if you need your repository to be private,
you should either use BitBucket instead of GitHub,
or use a GitHub paid plan.)

Create a `GitHub <https://github.com/>`__ account,
then create a repository for your project.
Leave the box unchecked for "Initialize this repository with a README".
After creating the repository, follow the instructions on the next page
to push your code to GitHub.


Docker Hub
----------

-   Go to `Docker Hub <https://hub.docker.com/>`__ and create an account.
-   Follow `these instructions <https://docs.docker.com/docker-hub/builds/>`__
    to create an automated build.
    In summary: in your account settings, go to "Linked Accounts & Services",
    and link your GitHub account.
    Then create an automated build for your GitHub repo.

Add Docker files and push to GitHub
-----------------------------------

On your local computer's command line, go to your project folder and run these commands to download
the 4 Docker files (should add them to the same folder as ``requirements.txt``).

If developing on Mac/Linux::

    curl https://raw.githubusercontent.com/oTree-org/otree-docker/master/Dockerfile > Dockerfile
    curl https://raw.githubusercontent.com/oTree-org/otree-docker/master/entrypoint.sh > entrypoint.sh
    curl https://raw.githubusercontent.com/oTree-org/otree-docker/master/pg_ping.py > pg_ping.py
    curl https://raw.githubusercontent.com/oTree-org/otree-docker/master/.dockerignore > .dockerignore

If developing on Windows::

    iwr https://raw.githubusercontent.com/oTree-org/otree-docker/master/Dockerfile -OutFile Dockerfile
    iwr https://raw.githubusercontent.com/oTree-org/otree-docker/master/entrypoint.sh -OutFile entrypoint.sh
    iwr https://raw.githubusercontent.com/oTree-org/otree-docker/master/pg_ping.py -OutFile pg_ping.py
    iwr https://raw.githubusercontent.com/oTree-org/otree-docker/master/.dockerignore -OutFile .dockerignore


Then run::

    git add .
    git commit -am "added docker files"
    git push origin master

Go to Docker Hub and ensure that the automatic build you set up was triggered.

Set up Docker on your server
----------------------------

Docker config files
~~~~~~~~~~~~~~~~~~~

Login to your server, and create a folder::

    mkdir otree-docker
    cd otree-docker


Run these commands to save the following 2 Docker files to that folder.

If your server is Linux/Mac::

    curl https://raw.githubusercontent.com/oTree-org/otree-docker/master/docker-compose.yaml > docker-compose.yaml
    curl https://raw.githubusercontent.com/oTree-org/otree-docker/master/.env > .env

If your server is Windows::

    iwr https://raw.githubusercontent.com/oTree-org/otree-docker/master/docker-compose.yaml -OutFile docker-compose.yaml
    iwr https://raw.githubusercontent.com/oTree-org/otree-docker/master/.env -OutFile .env

Open ``docker-compose.yaml`` and change the line with ``image:``
to use your Docker Hub user-name/repository-name, e.g.::

    image: YourDockerUsername/YourOTreeRepo:latest

Open ``.env``, and customize it as you wish.
You should decide what ``OTREE_PORT`` to use.
You should use port 80 if you are a superuser,
and especially if your site needs to be accessed from the internet.
Otherwise, you can use a higher port number like 8000, 8001, etc.

Install Docker Compose on the server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Note: These instructions assume you are installing Docker on Ubuntu Linux.

On your server:

Install Docker Engine::

    sudo apt-get update
    sudo apt install docker.io

Install docker-compose::

    sudo apt install python3-pip
    pip3 install docker-compose

Allow docker to be run without ``sudo``::

    sudo groupadd docker
    sudo usermod -aG docker $USER

Then logout for the changes to take effect.

Once you have logged back into your server, login to Docker with your Docker Hub
credentials::

    docker login

Download and run your image
~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

If you change your ``docker-compose.yaml`` or ``.env``,
you will need to recreate your container::

    docker-compose up --force-recreate

Sharing a server with other oTree users
---------------------------------------

If multiple users need to share a server,
you just need to create a separate folder with ``docker-compose.yaml`` and ``.env``
for each user.

If users need to run experiments simultaneously,
then each user should edit their ``.env`` file to set a
different ``OTREE_PORT``, e.g. 8000, 8001, etc.


Next steps
----------

See :ref:`server_final_steps` for steps you should take before launching your study.
