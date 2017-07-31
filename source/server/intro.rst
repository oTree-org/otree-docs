Server setup
============

If you are just testing your app on your personal computer, you can use
``otree runserver``. You don't need a full server setup.

However, when you want to share your app with an audience,
you must use a web server.

Choose which option you need:

**You want to launch your app to users on the internet**

Use :ref:`Heroku <heroku>`.
Heroku can also be used for lab/field studies, if you prefer cloud hosting over
using a local server.

**You want to use your Windows computer as an ad-hoc server on your local network**

e.g. running a lab study or field study.

-   Install the server using :ref:`Docker <install-docker-adhoc>` **OR** :ref:`conventional installation <install-windows>`
-   Set up your Windows PC as an :ref:`ad-hoc server <server-adhoc>`

**You want to use your Mac computer as an ad-hoc server on your local network**

e.g. running a lab study or field study.

-   Install the server using :ref:`Docker <install-docker-adhoc>` **OR** :ref:`conventional installation <install-mac>`
-   Set up your Mac as an :ref:`ad-hoc server <server-adhoc>`

**You want to set up a dedicated Linux server**

:ref:`Ubuntu Linux <server-ubuntu>` instructions.

**You want to deploy to a dedicated Linux/Windows server using Docker Hub**

:ref:`Docker Hub setup <dockerhub>`

**You want to see other options**

See :ref:`community` for some virtual machines created by oTree users.

**Next steps**
After setting up your server, see :ref:`server_final_steps`.

..  Consider removing the toctree because I think it's better for people to read
    through the instructions above, rather than jumping into a page they don't
    understand. Or, add info to the individual pages above, so incoming visitors
    don't bark up the wrong tree

.. toctree::
    :maxdepth: 2

    heroku.rst
    install-docker-adhoc.rst
    install-windows.rst
    install-mac.rst
    adhoc.rst
    ubuntu.rst
    dockerhub.rst
    next_steps.rst
    git.rst
