:orphan:

.. _otai:

OTAI (oTree AI Builder)
=======================

To build your apps with AI, go to `otreehub.com <https://www.otreehub.com>`__
and get started with OTAI.

Once you are ready to download and test the project you made, you should install oTree.

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
Then open PowerShell (on Windows) or Terminal (on Mac) to that folder
(you can use ``cd`` to navigate to the folder).

Enter this command at the prompt::

    pip3 install otree --upgrade

Step 3: Run the server
^^^^^^^^^^^^^^^^^^^^^^

In PowerShell or Terminal, go to the folder where you saved your project 
and run the server with ``otree devserver``.

Open your browser to `http://localhost:8000/ <http://localhost:8000/>`__.
You should see the oTree demo site with your apps / sessions listed.