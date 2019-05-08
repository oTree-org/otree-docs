.. _studio:

oTree Studio
============

`oTree Studio <https://www.otreehub.com/studio/>`__
is a new point-and-click interface for creating oTree projects.

If you are new to oTree,
you should consider using oTree Studio, because you can get started building
oTree apps without knowing Python.

How does oTree Studio work?
---------------------------

1.  Make an account on `oTree Hub <https://www.otreehub.com/studio>`__.
    oTree Studio is part of oTree Hub
    (the other part of oTree Hub is for Heroku server deployment)
1.  Build your app in oTree Studio's point-and-click interface.
    You can either create a new app or use one of the sample games.
2.  When you want to test your app, download your .otreezip file and run it
    on your computer or on Heroku.

How to build your app in oTree Studio
-------------------------------------

`Here <tutorial-studio>` is a tutorial showing how to make a simple app in oTree Studio.
The oTree documentation is written so it applies both to oTree Studio and the code-based
version.

How to test your app
--------------------

1.  Install Python and oTree, according to the simplified instructions in
    `oTree Studio <https://www.otreehub.com/studio/>`__'s download page.
    (It skips some steps from the conventional installation,
    such as running "otree startproject".)
2.  Open your command prompt and run ``otree runzip``. This will start your server.
3.  In oTree Studio, click the button to download your .otreezip file.
4.  The oTree server will automatically detect that the .otreezip file was downloaded,
    and run it. Note: you need to download the .otreezip file to the same folder where
    you ran ``otree runzip`` from.
5.  After making further changes to your app in oTree Studio, click "Download" again.
    The oTree server on your computer will automatically detect the updated .otreezip
    file, and run it.

.. _studio-otreezip

About .otreezip files
---------------------

.otreezip files are just regular oTree projects, compressed in a zip-like format.
If you want to see what is inside, run ``otree unzip``.
Inside, you will find the usual ``settings.py``, ``models.py``, ``pages.py``, HTML templates, etc.,
the same as if you had coded the project
by hand using Python.

This means that at any point if you want to switch from oTree Studio to editing the
Python/HTML code manually,
you just have to download your .otreezip and then run ``otree unzip my-project-name.otreezip``.
In other words, you are not "locked in" to oTree Studio.


Are all oTree features supported?
---------------------------------

Certain oTree features are currently omitted from oTree Studio,
especially less frequently used ones.
Those features will be added over time, as oTree Studio becomes more widely used.
If at any point you need to use one of these features, you are not stuck;
you can just download the code of your project and switch to using the Python-based
version of oTree. (But you cannot upload those changes back into oTree Studio.)

Can I upload my existing oTree apps into oTree Studio?
------------------------------------------------------

That is not currently supported,
as it is quite complicated to parse Python code.

Is oTree Studio stable?
-----------------------

oTree Studio is in beta. However, it is quite stable.
It is pretty low risk to use it because you can download the source code of your projects
and continue editing the Python code manually.