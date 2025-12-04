:orphan:

.. _install-windows:

Installing oTree
================

Important note
--------------

If you publish research done with oTree,
you are required to cite
`this paper <http://dx.doi.org/10.1016/j.jbef.2015.12.001>`__.
(Citation: Chen, D.L., Schonger, M., Wickens, C., 2016. oTree - An open-source
platform for laboratory, online and field experiments.
Journal of Behavioral and Experimental Finance, vol 9: 88-97)

Choose your editor
------------------

If you will build your apps with oTree Studio or OTAI (easiest option), go to `otreehub.com <https://www.otreehub.com>`__.
More info about using OTAI :ref:`here <otai>`.

If you have more programming experience, you can use oTree with a text editor.

oTree installation
------------------

Step 1: Install Python
^^^^^^^^^^^^^^^^^^^^^^^

Install Python from `python.org <https://www.python.org/>`__.
When installing, make sure to add Python to your PATH 
(otherwise you will get an error that the command "python" is not found).

Step 2: Install oTree
^^^^^^^^^^^^^^^^^^^^^

Create a folder where you will store your oTree projects. 
Then open PowerShell (on Windows) or Terminal (on Mac) to that folder.

Enter this command at the prompt::

    pip3 install otree --upgrade

Running the server
^^^^^^^^^^^^^^^^^^

Once you have a project,
start the server on your computer with ``otree devserver`` or (if using oTree Studio) ``otree zipserver``.

Open your browser to `http://localhost:8000/ <http://localhost:8000/>`__.
You should see the oTree demo site.

Using a text editor
^^^^^^^^^^^^^^^^^^^

Use ``otree startproject <name>`` to create a new project.
Use ``otree startapp <name>`` to create a new app.
