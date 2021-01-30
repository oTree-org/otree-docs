:orphan:

.. _install-macos:

Installing oTree on macOS
=========================

Important note
--------------

If you publish research conducted using oTree,
you are required by the oTree license to cite
`this paper <http://dx.doi.org/10.1016/j.jbef.2015.12.001>`__.
(Citation: Chen, D.L., Schonger, M., Wickens, C., 2016. oTree - An open-source
platform for laboratory, online and field experiments.
Journal of Behavioral and Experimental Finance, vol 9: 88-97)

If the below steps don't work for you, please email chris@otree.org with details.

Step 1: Install Python
----------------------

*   Download and install `Python <https://www.python.org/ftp/python/3.7.3/python-3.7.3-macosx10.6.pkg>`__
*   In Finder, search for and open the "Terminal" app:

.. figure:: _static/setup/macos-terminal.png

Step 2: Install oTree
---------------------

Enter this command at the prompt:

.. code-block:: bash

    pip3 install -U "otree>=5a"

.. note::

    This documentation is for oTree Lite. If you need maximum compatibility with existing oTree apps,
    switch to `this <https://otree.readthedocs.io/en/latest/index.html>`__ documentation.


Next steps
----------

-   If you will use :ref:`oTree Studio <studio>` (recommended),
    go to `otreehub.com <https://www.otreehub.com/studio>`__.
-   If you will use PyCharm or another text-based code editor,
    follow the steps :ref:`here <install-nostudio>`.
