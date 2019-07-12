.. _git-generic:

Set up Git
----------

If your code is on your personal computer and you are trying to push it to
your self-hosted web server, you can use Git.

On the server
~~~~~~~~~~~~~

On the server, create 2 directories -- one to store your project files,
and another to serve as the Git remote::

    mkdir oTree oTree.git

Create a git repo in ``oTree.git``::

    cd oTree.git
    git init --bare

Using a text editor such as ``nano``, add the following to
``oTree.git/hooks/post-receive``::

    #!/bin/sh
    GIT_WORK_TREE=/path/to/your/oTree
    export GIT_WORK_TREE
    git checkout -f

This means that every time someone pushes to ``oTree.git``, the code will be
checked out to the other folder ``oTree``. (This technique is further described
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
